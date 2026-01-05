# Multi-Agent Marketplace Simulation

**Autonomous AI agents trading in a simulated economy with emergent behaviors**

## 📋 Overview

This project implements a multi-agent marketplace where 20 AI agents with distinct personalities autonomously trade wood. Each agent uses LLM-powered reasoning (Llama 3.3 70B via Groq) to make buying and selling decisions based on:
- Current market conditions
- Personal budget and inventory
- Past trading experiences (memory system)
- Individual personality traits

## 🎯 Project Goals

- **Autonomous Agents**: Each agent makes independent decisions without central control
- **Emergent Behaviors**: Market dynamics arise from agent interactions (price discovery, speculation, panic selling)
- **Memory System**: Agents remember past trades and learn from experiences
- **Complete Ledger**: Track all transactions with full audit trail
- **Analytics**: Visualize market dynamics and agent performance

## 🏗️ Architecture

```
marketplace_simulation/
├── agents/
│   ├── agent.py          # TradingAgent class with LLM decision-making
│   ├── memory.py         # Memory system with temporal decay
│   └── roles.py          # 20 agent personality definitions
├── core/
│   └── market.py         # MarketWorld orchestration and ledger
├── visualization/
│   └── analytics.py      # Data analysis and plotting
├── logs/                 # Generated during simulation
│   ├── transaction_ledger.csv
│   ├── active_offers.json
│   └── *.png (charts)
├── simulation.py         # Main simulation runner
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Groq API key (free tier available at https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd marketplace_simulation

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Run Simulation

```bash
python simulation.py
```

The simulation will:
1. Initialize 20 agents with unique personalities
2. Run market cycles (default: 3 ticks)
3. Generate transaction logs
4. Create analytical charts and reports

## 📊 Outputs

After running the simulation, check the `logs/` directory:

### Data Files
- `transaction_ledger.csv` - Complete trade history with timestamps
- `active_offers.json` - Current market state

### Visualizations
- `price_evolution.png` - Price trends over time
- `trade_volume.png` - Cumulative and individual trade volumes
- `trader_activity.png` - Most active buyers and sellers
- `market_concentration.png` - Trading volume distribution
- `summary_report.txt` - Text summary with key statistics

## 👥 Agent Personalities

### Producers (Sellers)
- **Old_Tom**: Fair pricing, consistent seller
- **Young_Silas**: Impatient, quick price cuts
- **Industrial_Sawmill**: Bulk-only, high volume
- **Forest_Ranger_Ben**: Stable market advocate

### Consumers (Buyers)
- **City_Builder_Mark**: Urgent buyer, unlimited budget
- **Furniture_Maker_Ann**: Bargain hunter, price-sensitive
- **Poor_Carpenter_Dan**: Budget-constrained, desperate
- **Wealthy_Landowner**: Hoarder, price-insensitive

### Speculators
- **Scalper_Sam**: Buy low, sell high (2x markup)
- **Strategic_Steve**: Waits for supply shocks
- **Panic_Paul**: Emotional, dumps inventory

### Special Characters
- **Rational_Rita**: Data-driven, 5% price tolerance
- **Generous_Gina**: Sells at loss to help poor agents
- **The_Hermit**: Chaos agent, $1 wood dumps
- **Greedy_Gus**: 5x overpricing
- **Market_Bot_X**: Pure profit maximization
- **Village_Mayor**: Community-focused buyer

## 🧠 Technical Details

### Decision-Making Process

Each agent follows this cycle:
1. **Perceive**: View current market offers
2. **Remember**: Retrieve relevant past experiences
3. **Reason**: LLM generates decision with reasoning
4. **Act**: Execute buy/post/wait command
5. **Learn**: Store outcome in memory

### Memory System

Based on "Generative Agents" paper (Park et al., 2023):
- **Importance Scoring**: Critical events weighted higher (1-10 scale)
- **Temporal Decay**: Recent memories prioritized (0.99 decay factor)
- **Relevance Matching**: Partner-based retrieval
- **Top-K Selection**: Returns N most relevant memories

### Market Mechanics

- **No Central Pricing**: Prices emerge from supply/demand
- **Offer Board**: Agents post items for sale
- **Instant Execution**: Buyers accept offers immediately
- **Complete Ledger**: All trades permanently recorded

## 🔧 Configuration

### Simulation Parameters

Edit `simulation.py`:

```python
sim = MarketSimulation()
sim.run(total_ticks=10)  # Adjust number of rounds
```

### Agent Behavior

Edit `agents/roles.py` to modify budgets, inventories, or personalities.

### API Rate Limiting

Adjust sleep time in `simulation.py` (line 32):

```python
time.sleep(3)  # Seconds between agent actions
```

## 📈 Example Results

From a typical 3-tick simulation:
- **Total Trades**: 15-25 transactions
- **Price Range**: $0.10 - $50.00 per unit
- **Most Active**: City_Builder_Mark (buyer), Old_Tom (seller)
- **Emergent Behaviors**: Price wars, panic selling, strategic hoarding

## 🔬 Observed Emergent Behaviors

1. **Price Discovery**: Market converges to ~$5-10 per unit
2. **Speculation**: Scalper_Sam buys low and reposts higher
3. **Panic Cascades**: Panic_Paul triggers price drops
4. **Charity Economics**: Generous_Gina subsidizes poor buyers
5. **Market Manipulation**: The_Hermit causes chaos with $1 dumps

## 🐛 Known Limitations

- Single commodity (Wood only)
- No negotiation protocol (binary accept/reject)
- API rate limits constrain simulation speed
- Simple memory retrieval (no vector embeddings)

## 🛠️ Troubleshooting

### "No trades in ledger"
- Agents may all be waiting for better prices
- Try running more ticks (`total_ticks=10`)
- Check that agents have initial inventory in `roles.py`

### "API rate limit exceeded"
- Increase `time.sleep()` value in `simulation.py`
- Upgrade to Groq paid tier

### "Module not found: matplotlib"
```bash
pip install matplotlib seaborn
```

## 📚 Dependencies

```
groq>=0.4.0
python-dotenv>=1.0.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

## 🗺️ Roadmap

### Current Version (v0.1)
- ✅ 20 autonomous agents
- ✅ Memory system
- ✅ Transaction ledger
- ✅ Analytics and visualizations

### Upcoming Features
- [ ] Partial quantity purchases
- [ ] Smart multi-offer buying
- [ ] Additional commodities (Stone, Food)
- [ ] Negotiation protocol
- [ ] Vector-based memory retrieval
- [ ] Real-time web dashboard

## 📖 References

- [Generative Agents Paper](https://arxiv.org/abs/2304.03442) - Park et al., 2023
- [Agent Laboratory Framework](https://agentlaboratory.github.io/)
- [Groq API Documentation](https://console.groq.com/docs)

## 👨‍💻 Author

Created as part of a multi-agent systems challenge.

---

**Note**: The simulation demonstrates emergent economic behaviors arising from autonomous agent interactions. Results may vary based on LLM randomness and agent initialization.