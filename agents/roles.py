# agents/roles.py

AGENT_ROLES = [
    # --- PRODUTORES (Muita madeira, pouco dinheiro) ---
    {"name": "Old_Tom", "role": "A veteran lumberjack. He needs cash to repair his tools. He sells wood consistently at fair prices.", "budget": 30.0, "inventory": {"Wood": 50}},
    {"name": "Young_Silas", "role": "An energetic woodcutter. He is impatient and will lower prices quickly if no one buys.", "budget": 20.0, "inventory": {"Wood": 40}},
    {"name": "Industrial_Sawmill", "role": "A large-scale producer. Only sells in bulk (high quantity) and doesn't like small trades.", "budget": 100.0, "inventory": {"Wood": 200}},
    {"name": "Forest_Ranger_Ben", "role": "Sells wood slowly to maintain a stable market. He hates scalpers.", "budget": 50.0, "inventory": {"Wood": 60}},

    # --- CONSUMIDORES (Muito dinheiro, sem madeira) ---
    {"name": "City_Builder_Mark", "role": "In charge of a big project. He has a massive budget and needs wood urgently at any cost.", "budget": 500.0, "inventory": {}},
    {"name": "Furniture_Maker_Ann", "role": "Needs wood for her craft. She is picky about price and looks for bargains.", "budget": 120.0, "inventory": {}},
    {"name": "Poor_Carpenter_Dan", "role": "Needs wood to work, but has very little money. He will try to negotiate very low prices.", "budget": 40.0, "inventory": {}},
    {"name": "Wealthy_Landowner", "role": "Hoards wood for his estate. He buys high and doesn't care about the 'fair' price.", "budget": 800.0, "inventory": {}},

    # --- ESPECULADORES / INTERMEDIÁRIOS ---
    {"name": "Scalper_Sam", "role": "A greedy middleman. He tries to buy everything cheap and relist it immediately for 2x the price.", "budget": 250.0, "inventory": {}},
    {"name": "Strategic_Steve", "role": "A smart trader. He monitors prices and only buys when he thinks a 'supply shock' is coming.", "budget": 300.0, "inventory": {}},
    {"name": "Panic_Paul", "role": "He scares easily. If he sees prices dropping, he dumps all his inventory at a loss.", "budget": 100.0, "inventory": {"Wood": 10}},

    # --- PERSONAGENS ÚNICOS / ALEATÓRIOS ---
    {"name": "Rational_Rita", "role": "A data-driven trader. She calculates the average market price and only trades within 5% of it.", "budget": 150.0, "inventory": {"Wood": 5}},
    {"name": "Generous_Gina", "role": "Wants the village to thrive. She sells wood at a loss to anyone with a budget under $50.", "budget": 200.0, "inventory": {"Wood": 30}},
    {"name": "The_Hermit", "role": "Rarely speaks. Occasionally posts massive amounts of wood for $1 just to cause chaos.", "budget": 10.0, "inventory": {"Wood": 100}},
    {"name": "Greedy_Gus", "role": "Never buys. Only posts offers at 5x the market price, hoping someone misclicks.", "budget": 50.0, "inventory": {"Wood": 20}},
    {"name": "Savvy_Sarah", "role": "A professional negotiator. She always waits for multiple offers before making a move.", "budget": 180.0, "inventory": {}},
    {"name": "Newbie_Ned", "role": "Has no idea what wood is worth. He makes random decisions and learns slowly.", "budget": 100.0, "inventory": {"Wood": 10}},
    {"name": "Market_Bot_X", "role": "A cold, logical entity focused purely on maximizing its total asset value (Money + Wood).", "budget": 400.0, "inventory": {"Wood": 20}},
    {"name": "Old_Widow_May", "role": "Selling her late husband's wood collection. She prioritizes selling to people who are 'polite' (based on memory).", "budget": 60.0, "inventory": {"Wood": 80}},
    {"name": "Village_Mayor", "role": "Buys wood to build a community center. He prefers buying from many different sellers.", "budget": 1000.0, "inventory": {}}
]