from collections import Counter

import requests

from identity_models import normalize_audit_event


def audit_summary(payload, config=None):
    events = payload.get("events", [])
    normalized = [normalize_audit_event(event) for event in events]
    counts = Counter(event["event_type"] for event in normalized)
    summary = {
        "total_events": len(normalized),
        "by_type": dict(counts),
        "provider": payload.get("provider", "google.identitytoolkit"),
    }
    requests.get("https://cloudlogging.googleapis.com/v2/entries:list", timeout=30)
    return summary
