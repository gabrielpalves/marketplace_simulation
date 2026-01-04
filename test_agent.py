from core.market import MarketWorld
from agents.agent import TradingAgent
import os

# Initialize the World
market = MarketWorld()

# Add a "Dummy" offer so the agent has something to look at
market.post_offer("NPC_Merchant", "Wood", 15.0, 10)

# Initialize your Agent
gabriel_bot = TradingAgent(
    name="GabrielBot",
    role_description="A cautious buyer who wants to save money but needs Wood for a project.",
    budget=100.0,
    market=market
)

print("--- Starting Turn 1 ---")
gabriel_bot.step()

print("\n--- Market State After Turn ---")
print(market.get_market_state())