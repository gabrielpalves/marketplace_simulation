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
        
        print(f"✅ {len(self.agents)} agents initialized")

    def run_tick(self, tick_number):
        print(f"\n" + "="*50)
        print(f"🕒 MARKET TICK {tick_number}")
        print("="*50)
        
        # Random order for fairness
        random.shuffle(self.agents)
        
        for agent in self.agents:
            print(f"\n--- {agent.name} is thinking... ---")
            agent.step()
            # Small delay to avoid hitting Groq API rate limits
            # time.sleep(1)

        print(f"\n✅ End of Tick {tick_number}. Total Trades in Ledger: {len(self.market.ledger)}")

    def run(self, total_ticks=5):
        print("\n" + "="*70)
        print("🏛️  MULTI-AGENT MARKETPLACE SIMULATION")
        print("="*70)
        print(f"Total Agents: {len(self.agents)}")
        print(f"Total Ticks: {total_ticks}")
        print("="*70 + "\n")
        
        for i in range(1, total_ticks + 1):
            self.run_tick(i)
        
        print("\n" + "="*70)
        print("🏁 SIMULATION COMPLETE!")
        print("="*70)
        print(f"Total Trades: {len(self.market.ledger)}")
        print("📁 Logs saved to: logs/")
        print("  - transaction_ledger.csv")
        print("  - active_offers.json")
        print("\n📊 Generating analytics...")
        
        # Generate analytics automatically
        try:
            from visualization.analytics import MarketAnalytics
            analytics = MarketAnalytics()
            analytics.generate_all_reports()
        except ImportError:
            print("⚠️ Analytics module not found. Install matplotlib and seaborn:")
            print("   pip install matplotlib seaborn")
        except Exception as e:
            print(f"⚠️ Could not generate analytics: {e}")

if __name__ == "__main__":
    sim = MarketSimulation()
    sim.run(total_ticks=10)