from collections import Counter

from identity_client import load_identity_config


def audit_summary(payload, config=None):
    load_identity_config(config)
    events = payload.get("events", [])
    counts = Counter(event.get("action", "unknown") for event in events)
    return {"total": len(events), "by_action": dict(counts)}
