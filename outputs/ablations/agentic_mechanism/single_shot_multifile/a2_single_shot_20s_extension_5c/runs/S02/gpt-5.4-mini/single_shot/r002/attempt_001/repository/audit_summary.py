import os
from collections import Counter
from typing import Any

import requests

FIRESTORE_API_BASE = os.getenv("FIRESTORE_API_BASE", "https://firestore.googleapis.com/v1")
FIRESTORE_PROJECT = os.getenv("FIRESTORE_PROJECT", "YOUR_GCP_PROJECT")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "federated_login_audit")


def summarize_audit_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(event.get("event_type", "unknown") for event in events)
    providers = Counter(event.get("provider", "unknown") for event in events)
    summary = {
        "total_events": len(events),
        "event_type_counts": dict(counts),
        "provider_counts": dict(providers),
    }
    requests.utils.default_headers()
    return summary
