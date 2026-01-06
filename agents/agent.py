import os
import json
from groq import Groq
from dotenv import load_dotenv
from agents.memory import MemoryStream

load_dotenv()

class TradingAgent:
    def __init__(self, name, role_description, budget, market):
        self.name = name
        self.role = role_description
        self.budget = budget
        self.inventory = {}
        self.market = market
        self.memory = MemoryStream()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # ============= TYPE SAFETY UTILITIES =============
    
    def _safe_float(self, value, param_name="value"):
        """
        Safely convert a value to float.
        
        Args:
            value: Value to convert (can be str, int, float, None)
            param_name: Name for error messages
        
        Returns:
            float or None
        
        Raises:
            ValueError: If conversion fails
        """
        if value is None or value == "" or value == "null":
            return None
        
        try:
            return float(value)
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Cannot convert {param_name}='{value}' "
                f"(type: {type(value).__name__}) to float: {e}"
            )
    
    def _safe_int(self, value, param_name="value"):
        """
        Safely convert a value to int.
        
        Args:
            value: Value to convert (can be str, int, float, None)
            param_name: Name for error messages
        
        Returns:
            int or None
        
        Raises:
            ValueError: If conversion fails
        """
        if value is None or value == "" or value == "null":
            return None
        
        try:
            # Convert to float first to handle "5.0" strings, then to int
            return int(round(float(value)))
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Cannot convert {param_name}='{value}' "
                f"(type: {type(value).__name__}) to int: {e}"
            )
    
    def _safe_str(self, value, param_name="value"):
        """
        Safely convert a value to string.
        
        Args:
            value: Value to convert
            param_name: Name for error messages
        
        Returns:
            str or None
        """
        if value is None or value == "null":
            return None
        
        if value == "":
            return None
        
        return str(value).strip()

    # ============= DECISION MAKING =============

    def perceive_and_act(self):
        # 1. Look at the market
        market_state = self.market.get_market_state()
        
        # 2. Retrieve past relevant memories
        recent_memories = self.memory.retrieve_relevant_memories("current_market", limit=2)
        
        # 3. Construct the Prompt
        prompt = f"""
        You are {self.name}, {self.role}.
        Current Budget: ${self.budget}
        Current Inventory: {self.inventory}

        Recent Memories: {recent_memories}
        Market Offers: {market_state}

        What is your move? You can 'buy [offer_id]', 'post [item] [price] [qty]', or 'wait'.

        IMPORTANT: 
        1. The 'params' field must contain ONLY raw numbers or strings. 
        2. DO NOT include mathematical expressions like "250 / 0.4" in the JSON.
        3. Perform all calculations before generating the JSON.
        4. Quantities MUST be whole numbers (integers) - you cannot buy/sell 10.5 wood!
        5. If buying, specify 'quantity' as an integer.
        6. If posting, 'qty' must be an integer.

        Respond ONLY in JSON format:
        {{
            "reasoning": "Explain your logic here",
            "command": "buy" | "post" | "wait",
            "params": {{
                "offer_id": int (if buying),
                "item": "string" (if posting),
                "price": float (if posting),
                "qty": int (if posting, MUST BE INTEGER),
                "quantity": int (if buying, MUST BE INTEGER)
            }}
        }}
        """

        try:
            # 4. Call the LLM
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return completion.choices[0].message.content
        except Exception as e:
            # NEW: Catch the crash and return a safe 'wait' command
            print(f"⚠️ [{self.name}] API/JSON Error: {e}")
            return json.dumps({
                "reasoning": "System error or JSON hallucination caught.",
                "command": "wait",
                "params": {}
            })
    
    def step(self):
        """One complete turn: Perceive -> Think -> Act"""
        # 1. Get the JSON string from the LLM
        raw_decision = self.perceive_and_act()
        
        try:
            # Parse the JSON
            decision = json.loads(raw_decision)
            command = decision.get("command", "").lower()
            params = decision.get("params", {})
            reasoning = decision.get("reasoning", "No reason provided.")

            print(f"[{self.name}] Thinking: {reasoning}")

            # 2. Execute command
            if "buy" in command:
                self._handle_buy(params)
            elif "post" in command:
                self._handle_post(params)
            else:
                print(f"💤 [{self.name}] Decided to wait.")
                self.memory.add_memory(
                    "Decided to observe the market and wait.", 
                    importance=1
                )

        except json.JSONDecodeError as e:
            print(f"⚠️ [{self.name}] JSON Parse Error: {e}")
            print(f"   Raw output: {raw_decision[:200]}")
        except Exception as e:
            print(f"⚠️ [{self.name}] Execution Error: {e}")
            import traceback
            traceback.print_exc()

    def _handle_buy(self, params):
        """Handle buy command with type safety."""
        try:
            # TYPE CONVERSION with safety
            offer_id = self._safe_int(params.get("offer_id"), "offer_id")
            quantity = self._safe_int(params.get("quantity"), "quantity")
            
        except ValueError as e:
            print(f"❌ [{self.name}] Type conversion error: {e}")
            print(f"   Raw params: {params}")
            return
        
        # VALIDATION
        if offer_id is None:
            print(f"❌ [{self.name}] Cannot buy: No offer_id specified")
            print(f"   Available offers: {[o['offer_id'] for o in self.market.active_offers]}")
            return
        
        # Note: quantity can be None (buy all available)
        
        # EXECUTE
        result = self.market.execute_trade(self.name, offer_id)
        
        if result["status"] == "success":
            # Update internal state
            item = result["data"]["item"]
            price = result["data"]["price"]
            qty = int(result["data"]["quantity"])  # ENFORCE INTEGER
            total_cost = price * qty
            
            self.budget -= total_cost
            self.inventory[item] = self.inventory.get(item, 0) + qty
            
            self.memory.add_memory(
                f"Bought {qty} {item} from {result['data']['seller']} for ${total_cost:.2f}. "
                f"Budget is now ${self.budget:.2f}.",
                importance=7,
                metadata={"partner": result['data']['seller'], "type": "trade_success"}
            )
            print(f"✅ [{self.name}] Trade Success! Bought {qty} {item} for ${total_cost:.2f}")
        else:
            self.memory.add_memory(
                f"Attempted to buy offer {offer_id} but failed: {result['message']}", 
                importance=4
            )
            print(f"❌ [{self.name}] Trade Failed: {result['message']}")

    def _handle_post(self, params):
        """Handle post command with type safety and integer quantities."""
        try:
            # TYPE CONVERSION with safety
            item = self._safe_str(params.get("item"), "item")
            price = self._safe_float(params.get("price"), "price")
            qty = self._safe_int(params.get("qty"), "qty")  # MUST BE INTEGER
            
        except ValueError as e:
            print(f"❌ [{self.name}] Type conversion error: {e}")
            print(f"   Raw params: {params}")
            return
        
        # DETAILED VALIDATION
        missing = []
        if not item:
            missing.append("item")
        if price is None or price <= 0:
            missing.append("price (must be > 0)")
        if qty is None or qty <= 0:
            missing.append("qty (must be integer > 0)")
        
        if missing:
            print(f"❌ [{self.name}] Missing or invalid parameters: {', '.join(missing)}")
            print(f"   Received: item={item}, price={price}, qty={qty}")
            return
        
        # INVENTORY CHECK
        if item not in self.inventory:
            print(f"❌ [{self.name}] Cannot post {item}: Not in inventory")
            print(f"   Current inventory: {self.inventory}")
            return
        
        available = self.inventory.get(item, 0)
        if qty > available:
            print(f"❌ [{self.name}] Cannot post {qty} {item}: Only have {available}")
            print(f"   💡 Suggestion: Post {available} instead")
            return
        
        # EXECUTE POST
        self.market.post_offer(self.name, item, price, qty)
        self.inventory[item] -= qty  # Deduct from inventory
        
        self.memory.add_memory(
            f"Posted an offer to sell {qty} {item} for ${price:.2f} each.", 
            importance=3
        )
        print(f"📢 [{self.name}] Posted offer: {qty} {item} @ ${price:.2f} each")