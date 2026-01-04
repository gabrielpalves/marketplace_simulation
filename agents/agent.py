import os
import json
from groq import Groq
from dotenv import load_dotenv
from agents.memory import MemoryStream

load_dotenv()

class TradingAgent:
    def __init__(self, name, role_description, budget, market):
        self.name = name
        self.role = role_description  # e.g., "The Greedy Scalper"
        self.budget = budget
        self.inventory = {}
        self.market = market
        self.memory = MemoryStream()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def perceive_and_act(self):
        # 1. Look at the market
        market_state = self.market.get_market_state()
        
        # 2. Retrieve past relevant memories (The 2023 paper logic)
        recent_memories = self.memory.retrieve_relevant_memories("current_market", limit=2)
        
        # 3. Construct the Prompt
        prompt = f"""
        You are {self.name}, {self.role}.
        Current Budget: ${self.budget}
        Current Inventory: {self.inventory}
        
        Recent Memories: {recent_memories}
        Market Offers: {market_state}
        
        What is your move? You can 'buy [offer_id]', 'post [item] [price] [qty]', or 'wait'.
        Respond ONLY in JSON format:
        {{"reasoning": "...", "command": "...", "params": {{}}}}
        """

        # 4. Call the LLM
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        decision = completion.choices[0].message.content
        return decision
    
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

            # 2. The Execution Layer (The 'Act' part)
            if "buy" in command:
                offer_id = params.get("offer_id")
                result = self.market.execute_trade(self.name, offer_id)
                if result["status"] == "success":
                    # Update internal state if trade was successful
                    item = result["data"]["item"]
                    price = result["data"]["price"]
                    self.budget -= price
                    self.inventory[item] = self.inventory.get(item, 0) + result["data"]["quantity"]
                    self.memory.add_memory(f"Bought {item} for ${price}", importance=5)
                    print(f"✅ Trade Successful! New Budget: ${self.budget}")
                else:
                    print(f"❌ Trade Failed: {result['message']}")

            elif "post" in command:
                item = params.get("item")
                price = params.get("price")
                qty = params.get("qty")
                self.market.post_offer(self.name, item, price, qty)
                self.memory.add_memory(f"Posted {qty} {item} for ${price}", importance=3)
                print(f"📢 Posted offer for {qty} {item}")

            else:
                print("💤 Agent decided to wait.")
                self.memory.add_memory("Decided to observe the market and wait.", importance=1)

        except Exception as e:
            print(f"⚠️ Error parsing agent decision: {e}")