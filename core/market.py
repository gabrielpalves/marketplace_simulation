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
        
        # Initialize an empty Ledger
        self.ledger = pd.DataFrame(columns=[
            "timestamp", "seller", "buyer", "item", "price", "quantity"
        ])
        
        # Active offers on the "Bulletin Board"
        self.active_offers = []

    def post_offer(self, seller_name, item, price, quantity):
        """Allows an agent to list something for sale."""
        offer = {
            "offer_id": len(self.active_offers) + 1,
            "seller": seller_name,
            "item": item,
            "price": price,
            "quantity": quantity,
            "timestamp": datetime.now().isoformat()
        }
        self.active_offers.append(offer)
        self._save_offers()
        return offer["offer_id"]

    def execute_trade(self, buyer_name, offer_id):
        """Processes a transaction between a buyer and an active offer."""
        offer = next((o for o in self.active_offers if o["offer_id"] == offer_id), None)
        
        if not offer:
            return {"status": "error", "message": "Offer not found"}

        # Record in Ledger
        new_trade = {
            "timestamp": datetime.now().isoformat(),
            "seller": offer["seller"],
            "buyer": buyer_name,
            "item": offer["item"],
            "price": offer["price"],
            "quantity": offer["quantity"]
        }
        
        # Add to pandas dataframe and save to CSV
        self.ledger = pd.concat([self.ledger, pd.DataFrame([new_trade])], ignore_index=True)
        self.ledger.to_csv(self.ledger_path, index=False)
        
        # Remove offer from active board
        self.active_offers.remove(offer)
        self._save_offers()
        
        return {"status": "success", "data": new_trade}

    def get_market_state(self):
        """Returns the current board for agents to see."""
        return self.active_offers

    def _save_offers(self):
        """Helper to keep a JSON 'trace' of current market state."""
        with open(self.offers_path, "w") as f:
            json.dump(self.active_offers, f, indent=4)