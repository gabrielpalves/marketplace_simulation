import pandas as pd
from datetime import datetime
import json
import os

class MarketWorld:
    def __init__(self):
        self.ledger_path = "logs/transaction_ledger.csv"
        self.offers_path = "logs/active_offers.json"
        
        # Ensure log directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Initialize empty DataFrame (no columns upfront to avoid FutureWarning)
        self.ledger = pd.DataFrame()
        
        # Active offers on the "Bulletin Board"
        self.active_offers = []
        self.offer_counter = 0  # Monotonic counter

    def post_offer(self, seller_name, item, price, quantity):
        """
        Allows an agent to list something for sale.
        
        Args:
            seller_name: Name of the seller
            item: Item to sell
            price: Price per unit (float)
            quantity: Quantity to sell (will be converted to int)
        
        Returns:
            offer_id (int)
        """
        self.offer_counter += 1
        
        # ENFORCE INTEGER QUANTITY
        qty_int = int(round(float(quantity)))
        
        if qty_int <= 0:
            print(f"⚠️ Warning: {seller_name} tried to post {quantity} units. Adjusted to {qty_int}.")
            return None
        
        offer = {
            "offer_id": self.offer_counter,
            "seller": seller_name,
            "item": item,
            "price": float(price),
            "quantity": qty_int,  # INTEGER
            "timestamp": datetime.now().isoformat()
        }
        self.active_offers.append(offer)
        self._save_offers()
        return offer["offer_id"]

    def execute_trade(self, buyer_name, offer_id):
        """
        Processes a transaction between a buyer and an active offer.
        
        Args:
            buyer_name: Name of the buyer
            offer_id: ID of the offer to purchase
        
        Returns:
            dict with status, message, and data
        """
        offer = next((o for o in self.active_offers if o["offer_id"] == offer_id), None)
        
        if not offer:
            return {"status": "error", "message": "Offer not found"}

        # Record in Ledger (with INTEGER quantity)
        new_trade = {
            "timestamp": datetime.now().isoformat(),
            "seller": offer["seller"],
            "buyer": buyer_name,
            "item": offer["item"],
            "price": float(offer["price"]),
            "quantity": int(offer["quantity"])  # ENFORCE INTEGER
        }
        
        # Add to ledger (fixed to avoid FutureWarning)
        new_row = pd.DataFrame([new_trade])
        
        if self.ledger.empty:
            # First trade - just assign
            self.ledger = new_row
        else:
            # Subsequent trades - concatenate
            self.ledger = pd.concat([self.ledger, new_row], ignore_index=True)
        
        self.ledger.to_csv(self.ledger_path, index=False)
        
        # Remove offer from active board
        self.active_offers.remove(offer)
        self._save_offers()
        
        return {"status": "success", "data": new_trade}

    def get_market_state(self):
        """
        Returns the current board for agents to see.
        
        Returns:
            list of active offers
        """
        return self.active_offers

    def _save_offers(self):
        """Helper to keep a JSON 'trace' of current market state."""
        with open(self.offers_path, "w") as f:
            json.dump(self.active_offers, f, indent=4)