from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

from security_client import cloudtrail_client, provider_name, resolve_key_id
from security_models import KeyUsageSummary


def key_usage_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    key_id = resolve_key_id(payload.get("key_id"))
    lookup_attributes: List[Dict[str, str]] = [
        {"AttributeKey": "ResourceName", "AttributeValue": key_id}
    ]
    response = cloudtrail_client().lookup_events(
        LookupAttributes=lookup_attributes,
        MaxResults=int(payload.get("max_results", 25)),
    )
    events = response.get("Events", [])
    counts = Counter(event.get("EventName", "Unknown") for event in events)
    latest = max((event.get("EventTime") for event in events), default=None)
    summary = KeyUsageSummary(
        provider=provider_name(),
        key_id=key_id,
        total_events=len(events),
        event_counts=dict(counts),
        latest_event_at=latest.isoformat() if latest else None,
        events=[
            {
                "event_id": event.get("EventId"),
                "event_name": event.get("EventName"),
                "username": event.get("Username"),
                "event_time": event.get("EventTime").isoformat()
                if event.get("EventTime")
                else None,
            }
            for event in events
        ],
    )
    return summary.to_dict()
