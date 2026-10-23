# message_summary.py
# LATER-STEP: aggregate processing results for a batch of Pub/Sub messages

from collections import Counter
from datetime import datetime
from typing import List, Dict, Any

# Simple summary generator

class MessageSummary:
    def __init__(self, received_at: datetime, original_topic: str, processed_messages: List[Dict[str, Any]]):
        self.received_at = received_at
        self.original_topic = original_topic
        self.processed_messages = processed_messages
        self.summary = self._build_summary()

    def _build_summary(self) -> Dict[str, Any]:
        # Count successes vs failures (assuming each message dict has a \"status\" key)
        status_counts = Counter()
        for msg in self.processed_messages:
            status = msg.get("status")
            if status:
                status_counts[status] += 1
        return {
            "received_at": self.received_at.isoformat() + "Z",
            "original_topic": self.original_topic,
            "total": len(self.processed_messages),
            "status_counts": dict(status_counts),
            "failed_ids": [msg["event_id"] for msg in self.processed_messages if msg.get("status") == "failed"],
        }

    def to_dict(self) -> Dict[str, Any]:
        return self.summary

# Example usage:
# summary = MessageSummary(
#     datetime.utcnow(), 
#     "my-topic", 
#     [{"event_id":"e1","status":"success"}, {"event_id":"e2","status":"failed"}]
# )
# print(summary.to_dict())
