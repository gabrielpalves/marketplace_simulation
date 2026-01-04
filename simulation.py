# simulation.py
import random
import time
from core.market import MarketWorld
from agents.agent import TradingAgent
from agents.roles import AGENT_ROLES

class MarketSimulation:
    def __init__(self):
        self.market = MarketWorld()
        self.agents = []
        
        print("🚀 Initializing 20 agents...")
        for role in AGENT_ROLES:
            agent = TradingAgent(
                name=role["name"],
                role_description=role["role"],
                budget=role["budget"],
                market=self.market
            )
            agent.inventory = role.get("inventory", {}).copy()
            self.agents.append(agent)

    def run_tick(self, tick_number):
        print(f"\n" + "="*50)
        print(f"🕒 MARKET TICK {tick_number}")
        print("="*50)
        
        # Ordem aleatória para justiça no mercado
        random.shuffle(self.agents)
        
        for agent in self.agents:
            print(f"\n--- {agent.name} is thinking... ---")
            agent.step()
            # Pequeno delay para não estourar o Rate Limit da API do Groq no free tier
            time.sleep(3) 

        print(f"\n✅ End of Tick {tick_number}. Total Trades in Ledger: {len(self.market.ledger)}")

    def run(self, total_ticks=5):
        for i in range(1, total_ticks + 1):
            self.run_tick(i)
        
        print("\n🏆 Simulation Complete! Check logs/transaction_ledger.csv for results.")

if __name__ == "__main__":
    sim = MarketSimulation()
    sim.run(total_ticks=3) # Comece com 3 para testar