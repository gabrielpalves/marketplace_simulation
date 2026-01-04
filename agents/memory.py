import time
from datetime import datetime

class MemoryEntry:
    def __init__(self, content, importance, metadata=None):
        self.content = content      # e.g., "Sold 5 Wood to Agent_X for $50"
        self.importance = importance # 1 to 10 scale
        self.timestamp = time.time()
        self.metadata = metadata or {} # e.g., {"partner": "Agent_X", "item": "Wood"}

class MemoryStream:
    def __init__(self, decay_factor=0.99):
        self.entries = []
        self.decay_factor = decay_factor # How fast memories "fade"

    def add_memory(self, content, importance, metadata=None):
        entry = MemoryEntry(content, importance, metadata)
        self.entries.append(entry)

    def retrieve_relevant_memories(self, current_query, partner_name=None, limit=3):
        """
        A simplified retrieval system. 
        In 2026, we'd use Vector Embeddings, but for a clean 
        coding test, a logic-based search is often more transparent.
        """
        scored_memories = []
        now = time.time()

        for entry in self.entries:
            # 1. Recency Score (Exponential decay)
            hours_passed = (now - entry.timestamp) / 3600
            recency_score = self.decay_factor ** hours_passed
            
            # 2. Importance Score (Normalized 0-1)
            importance_score = entry.importance / 10
            
            # 3. Relevance Score (Simple keyword/metadata match)
            relevance_score = 0
            if partner_name and entry.metadata.get("partner") == partner_name:
                relevance_score = 1.0
            
            # Final Score Calculation
            final_score = recency_score + importance_score + relevance_score
            scored_memories.append((final_score, entry))

        # Sort by score and return the top 'limit' memories
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [m[1].content for m in scored_memories[:limit]]
