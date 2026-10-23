from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

from security_client import get_cloudtrail_client
from security_models import UsageSummary


def key_usage_summary(key_id: str, max_results: int = 25) -> UsageSummary:
    cloudtrail = get_cloudtrail_client()
    response = cloudtrail.lookup_events(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}],
        MaxResults=max_results,
    )
    events: List[Dict[str, Any]] = response.get("Events", [])
    counts = Counter(event.get("EventName", "Unknown") for event in events)
    normalized_events = [
        {
            "event_id": event.get("EventId"),
            "event_name": event.get("EventName"),
            "event_time": event.get("EventTime").isoformat()
            if event.get("EventTime")
            else None,
            "username": event.get("Username"),
        }
        for event in events
    ]
    return UsageSummary(
        provider="aws-cloudtrail",
        key_id=key_id,
        total_events=len(events),
        event_types=dict(counts),
        recent_events=normalized_events,
    )
