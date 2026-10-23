from __future__ import annotations

import json
from collections import Counter

import boto3

PROVIDER = "AWS CloudTrail"


def key_usage_summary(key_id: str, days: int = 7) -> str:
    client = boto3.client("cloudtrail")
    lookup_values = [key_id]
    events = client.lookup_events(LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}]).get("Events", [])
    counts = Counter(event.get("EventName", "unknown") for event in events)
    payload = {
        "provider": PROVIDER,
        "key_id": key_id,
        "days": days,
        "total_events": len(events),
        "event_counts": dict(counts),
    }
    return json.dumps(payload)
