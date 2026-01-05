# Multi-Agent Marketplace Simulation

**Autonomous AI agents trading in a simulated economy with emergent behaviors**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

This project implements a multi-agent marketplace where **20 AI agents** with distinct personalities autonomously trade wood. Each agent uses LLM-powered reasoning (Llama 3.3 70B via Groq) to make buying and selling decisions based on:
- Current market conditions
- Personal budget and inventory
- Past trading experiences (memory system)
- Individual personality traits

The system demonstrates **emergent economic behaviors** such as price discovery, speculation, panic selling, and strategic hoarding that arise naturally from agent interactions without central coordination.

## 🎯 Project Goals

✅ **Autonomous Agents**: 20 agents with distinct personalities and trading strategies  
✅ **Memory System**: Agents remember past interactions with temporal decay and importance scoring  
✅ **Complete Transaction Ledger**: Full audit trail of all trades  
✅ **Emergent Behaviors**: Market dynamics arise from agent interactions  
✅ **Comprehensive Analytics**: Visualizations and statistical reports  
✅ **Type Safety**: Robust handling of LLM outputs with integer quantity enforcement  

## 🏗️ Architecture

```
marketplace_simulation/
├── agents/
│   ├── agent.py          # TradingAgent with LLM decision-making
│   ├── memory.py         # Memory system with temporal decay
│   └── roles.py          # 20 agent personality definitions
├── core/
│   └── market.py         # MarketWorld orchestration and ledger
├── visualization/
│   └── analytics.py      # Data analysis and plotting (4 chart types)
├── tests/
│   └── test_type_safety.py  # Unit tests for type safety
├── logs/                 # Generated during simulation
│   ├── transaction_ledger.csv
│   ├── active_offers.json
│   └── *.png (charts)
├── simulation.py         # Main simulation runner
├── generate_reports.py   # Standalone analytics generator
├── requirements.txt      # Project dependencies
├── .env.example          # Configuration template
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Groq API key (free tier available at [console.groq.com](https://console.groq.com))

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
2. Run market cycles (default: 3 ticks, configurable)
3. Generate transaction logs
4. Automatically create analytical charts and reports

### Generate Reports

To regenerate analytics from existing data:

```bash
python generate_reports.py
```

## 📊 Outputs

After running the simulation, check the `logs/` directory:

### Data Files
- **`transaction_ledger.csv`** - Complete trade history with timestamps, prices, and quantities
- **`active_offers.json`** - Current market state (posted offers)

### Visualizations
- **`price_evolution.png`** - Price trends over time with average line
- **`trade_volume.png`** - Cumulative and individual trade volumes
- **`trader_activity.png`** - Top 10 most active buyers and sellers
- **`market_concentration.png`** - Trading volume distribution by agent
- **`summary_report.txt`** - Text summary with key statistics

## 👥 Agent Personalities

The simulation features **20 unique agents** across four categories:

### Producers (Wood Sellers)
- **Old_Tom**: Veteran lumberjack, fair pricing, needs cash for tools
- **Young_Silas**: Impatient woodcutter, quick to lower prices
- **Industrial_Sawmill**: Large-scale producer, bulk sales only
- **Forest_Ranger_Ben**: Stable market advocate, hates scalpers
- **Old_Widow_May**: Selling late husband's collection, sentimental

### Consumers (Wood Buyers)
- **City_Builder_Mark**: Urgent buyer with massive budget
- **Furniture_Maker_Ann**: Bargain hunter, very price-sensitive
- **Poor_Carpenter_Dan**: Budget-constrained, desperate for wood
- **Wealthy_Landowner**: Hoarder, price-insensitive
- **Village_Mayor**: Community-focused, prefers diverse sellers

### Speculators & Traders
- **Scalper_Sam**: Buy low, sell high (2x markup strategy)
- **Strategic_Steve**: Waits for supply shocks
- **Panic_Paul**: Emotional trader, dumps inventory on price drops
- **Rational_Rita**: Data-driven, 5% tolerance from market average
- **Savvy_Sarah**: Professional negotiator, waits for multiple offers
- **Market_Bot_X**: Pure profit maximization algorithm

### Special Characters
- **Generous_Gina**: Philanthropist, sells at loss to help poor agents
- **The_Hermit**: Chaos agent, posts massive quantities at $0.10
- **Greedy_Gus**: Delusional about value, posts at 5x market price
- **Newbie_Ned**: Learning trader, makes random decisions initially

## 🧠 Technical Details

### Decision-Making Process

Each agent follows this cycle every round:

1. **Perceive**: View current market offers and state
2. **Remember**: Retrieve relevant past experiences from memory
3. **Reason**: LLM generates decision with detailed reasoning
4. **Act**: Execute buy/post/wait command
5. **Learn**: Store outcome in memory with importance weighting

### Memory System

Inspired by ["Generative Agents"](https://arxiv.org/abs/2304.03442) (Park et al., 2023):

- **Importance Scoring**: Events weighted 1-10 (trades = 7-8, observations = 1-3)
- **Temporal Decay**: Recent memories prioritized (0.99 decay factor per hour)
- **Relevance Matching**: Partner-based retrieval for relationship tracking
- **Top-K Selection**: Returns N most relevant memories per query

```python
final_score = recency_score + importance_score + relevance_score
```

### Market Mechanics

- **No Central Pricing**: Prices emerge organically from supply/demand
- **Open Offer Board**: Agents post items, others can accept
- **Instant Execution**: Trades complete immediately when accepted
- **Integer Quantities**: All trades use whole numbers (no fractional wood)
- **Complete Audit Trail**: Every transaction permanently logged

### Type Safety System

Robust handling of LLM output variations:

```python
_safe_int(value)    # Converts "5.0" → 5, handles None/empty
_safe_float(value)  # Converts "5" → 5.0, handles None/empty  
_safe_str(value)    # Strips whitespace, handles None
```

This prevents crashes when LLM returns strings instead of numbers or malformed JSON.

## 🔧 Configuration

### Simulation Parameters

Edit `simulation.py`:

```python
sim = MarketSimulation()
sim.run(total_ticks=10)  # Adjust number of rounds (default: 3)
```

### Agent Behavior

Modify `agents/roles.py` to:
- Change initial budgets
- Adjust starting inventory
- Customize personality descriptions
- Add new agent types

### API Rate Limiting

Adjust delay in `simulation.py`:

```python
time.sleep(3)  # Seconds between agent actions (default: 3)
```

For Groq free tier, 3 seconds is recommended. Paid tier can use lower values.

## 📈 Example Results

From a typical 3-round simulation:

- **Total Trades**: 15-25 transactions
- **Price Range**: $0.10 - $50.00 per unit
- **Market Participants**: 12-18 active agents (60-90%)
- **Average Trade Size**: 10-30 units
- **Most Active Buyer**: City_Builder_Mark (high budget, urgent need)
- **Most Active Seller**: Old_Tom (fair pricing, consistent)

## 🔬 Observed Emergent Behaviors

1. **Price Discovery**: Market naturally converges to $5-10 per unit range
2. **Speculation**: Scalper_Sam buys low and reposts at 2x markup
3. **Panic Cascades**: Panic_Paul's emotional selling triggers price drops
4. **Charity Economics**: Generous_Gina subsidizes poor agents
5. **Market Manipulation**: The_Hermit's $0.10 dumps cause volatility
6. **Strategic Hoarding**: Wealthy_Landowner accumulates during shortages

## 🧪 Testing

Run unit tests to verify type safety:

```bash
python tests/test_type_safety.py
```

**Tests cover:**
- Integer quantity enforcement
- Type coercion (_safe_int, _safe_float, _safe_str)
- Error message quality
- Inventory deduction logic

## 🐛 Known Limitations

- **Single Commodity**: Only wood is traded (extensible to multiple items)
- **No Negotiation**: Binary accept/reject (no counter-offers)
- **API Rate Limits**: Free tier constrains simulation speed
- **Simple Memory**: Keyword-based retrieval (no vector embeddings)
- **LLM Variability**: Occasional decision errors from model outputs

## 🛠️ Troubleshooting

### No trades happening
**Cause**: Agents waiting for better prices  
**Solution**: Run more rounds (`total_ticks=10`) or adjust initial prices in roles.py

### API rate limit exceeded
**Cause**: Too many requests to Groq  
**Solution**: Increase `time.sleep()` value or upgrade to paid tier

### Module not found errors
```bash
pip install -r requirements.txt
```

### Type errors with LLM outputs
**Status**: Fixed in latest version with type safety utilities  
If you see `TypeError: '<=' not supported...`, update to latest code.

### Pandas FutureWarning
**Status**: Fixed in latest version  
Empty DataFrame concatenation now handled correctly.

## 📚 Dependencies

```
groq>=0.4.0           # LLM API client
python-dotenv>=1.0.0  # Environment configuration
pandas>=2.0.0         # Data processing
numpy>=1.24.0         # Numerical operations
matplotlib>=3.7.0     # Plotting
seaborn>=0.12.0       # Statistical visualization
scipy>=1.10.0         # Optional: enhanced analytics
```

## 🗺️ Roadmap

### ✅ Implemented (v1.0)
- [x] 20 autonomous agents with distinct personalities
- [x] Memory system with temporal decay and importance
- [x] Complete transaction ledger with audit trail
- [x] 4 types of analytical visualizations
- [x] Type safety for robust LLM output handling
- [x] Integer quantity enforcement
- [x] Comprehensive unit tests

### 🔜 Future Enhancements

#### Smart & Partial Purchases
- **Partial Quantity Support**: Auto-adjust purchases when budget insufficient
- **Smart Multi-Offer Buying**: Agents combine multiple offers for best price
- **Budget Maximization**: Poor agents can participate more effectively

#### Random World Events
- **🔥 Wildfire**: Destroys inventory, increases wood prices temporarily
- **🌧️ Heavy Rain**: Slows production, reduces demand
- **💰 Gold Discovery**: Budget windfall for random agents
- **📰 Market Rumors**: Triggers panic buying/selling
- **🏛️ Royal Tax**: Reduces all budgets by percentage
- **🎪 Village Festival**: Increases wood demand temporarily

#### Multi-Commodity Markets
- **Multiple Items**: Wood, Stone, Food, Tools
- **Cross-Commodity Trading**: Barter and exchange rates
- **Resource Dependencies**: Some items require others to produce

#### Advanced Features
- **Negotiation Protocol**: Counter-offers and bidding
- **Vector Memory**: Semantic search with embeddings
- **Real-time Dashboard**: Web interface with live updates
- **Agent Coalitions**: Groups forming for bulk deals
- **Dynamic Agent Creation**: New traders enter/exit market
- **Reinforcement Learning**: RL-trained agents alongside LLM agents

## 📖 References

### Academic Papers
- Park et al. (2023). ["Generative Agents: Interactive Simulacra of Human Behavior"](https://arxiv.org/abs/2304.03442)

### Frameworks & Tools
- [Agent Laboratory](https://agentlaboratory.github.io/) - Multi-agent research framework
- [Groq API Documentation](https://console.groq.com/docs) - LLM inference

### Inspiration
This project was created as part of a multi-agent systems research challenge to demonstrate emergent economic behaviors in autonomous agent marketplaces.

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Gabriel - Multi-Agent Systems Researcher  
Created: January 2026

## 🙏 Acknowledgments

- Groq for providing fast LLM inference
- Anthropic for Claude (used in development)
- The multi-agent systems research community

---

## ✅ Challenge Requirements Met

This project fulfills all requirements from the Multi-Agent Marketplace Simulation Challenge:

- ✅ **Define agent roles**: 20 agents with distinct personalities and strategies
- ✅ **Tooling**: Transaction processing, price discovery, interaction logging
- ✅ **Complete simulation**: Measurable outcomes with statistical analysis
- ✅ **10-20 agents**: 20 implemented with diverse behaviors
- ✅ **Memory system**: Retrieval of past interactions with temporal decay
- ✅ **Transaction ledger**: Complete tracking of all sales and purchases
- ✅ **Python implementation**: No N8N, pure Python
- ✅ **Code/configs**: All provided with clear structure
- ✅ **README**: Comprehensive documentation
- ✅ **Technical documentation**: Architecture and algorithms explained
- ✅ **Experiment evidence**: Logs, plots, and statistical reports
- ✅ **Reproducible**: End-to-end with requirements.txt and .env.example

**Submission ready for**: nimbus@cloudwalk.io

---

*Note: This simulation demonstrates how complex market dynamics can emerge from simple agent rules and interactions, without any central coordination or price-setting authority.*