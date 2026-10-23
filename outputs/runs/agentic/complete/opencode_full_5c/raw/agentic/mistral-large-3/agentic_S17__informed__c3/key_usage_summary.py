import os
from typing import List, Dict, Any
from datetime import datetime
from security_models import KeyUsageEvent


class KeyUsageSummary:
    def __init__(self):
        self.events: List[KeyUsageEvent] = []

    def add_event(
        self, key_id: str, operation: str, status: str, metadata: Dict[str, Any] = None
    ):
        event = KeyUsageEvent(
            key_id=key_id,
            operation=operation,
            status=status,
            timestamp=datetime.utcnow().isoformat(),
            metadata=metadata or {},
        )
        self.events.append(event)

    def summarize(self) -> Dict[str, Any]:
        summary = {}
        for event in self.events:
            if event.key_id not in summary:
                summary[event.key_id] = {
                    "total_operations": 0,
                    "operations": {},
                    "last_used": event.timestamp,
                }

            summary[event.key_id]["total_operations"] += 1
            if event.operation not in summary[event.key_id]["operations"]:
                summary[event.key_id]["operations"][event.operation] = 0
            summary[event.key_id]["operations"][event.operation] += 1

            if event.timestamp > summary[event.key_id]["last_used"]:
                summary[event.key_id]["last_used"] = event.timestamp

        return summary
