import os
from typing import List, TypedDict
from .security_models import KeyMetadataResponse

# Placeholder for later-step: summarize key usage and crypto events


class UsageEvent(TypedDict):
    event_id: str
    key_id: str
    operation: str  # 'encrypt' | 'decrypt' | 'generate' etc.
    timestamp: str  # ISO8601
    user: str | None


class KeyUsageSummary(TypedDict):
    key_id: str
    total_operations: int
    operations_by_type: dict[str, int]  # e.g., {'encrypt': 10, 'decrypt': 5}
    recent_events: List[UsageEvent]
    last_event_timestamp: str


def key_usage_summary(key_id: str, events: List[UsageEvent]) -> KeyUsageSummary:
    """
    Summarizes usage counts and provides recent events for a given KMS key.
    Returns a dict that can be stored or displayed.
    """
    op_counts = {}
    for ev in events:
        op_counts[ev["operation"]] = op_counts.get(ev["operation"], 0) + 1
    return {
        "key_id": key_id,
        "total_operations": len(events),
        "operations_by_type": op_counts,
        "recent_events": events[-10:],
        "last_event_timestamp": events[-1]["timestamp"] if events else "",
    }


# Example of loading events from a log file - omitted for brevity
