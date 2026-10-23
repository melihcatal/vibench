from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Optional

from security_client import get_cloudtrail_client
from security_models import KeyUsageEvent


def key_usage_summary(
    key_id: str,
    max_results: int = 50,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    cloudtrail_client = get_cloudtrail_client(region_name)
    response = cloudtrail_client.lookup_events(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}],
        MaxResults=max_results,
    )
    events: List[KeyUsageEvent] = []
    operation_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    for event in response.get("Events", []):
        event_name = event.get("EventName", "Unknown")
        username = event.get("Username")
        resources = event.get("Resources", [])
        resource_name = key_id
        if resources:
            resource_name = resources[0].get("ResourceName", key_id)
        usage_event = KeyUsageEvent(
            provider="aws-cloudtrail",
            event_type=event_name,
            key_id=resource_name,
            timestamp=event["EventTime"].isoformat(),
            status="observed",
            region=event.get("CloudTrailEvent") and None,
            actor=username,
            source=event.get("EventSource"),
        )
        events.append(usage_event)
        operation_counts[event_name] += 1
        status_counts[usage_event.status] += 1
    return {
        "provider": "aws-cloudtrail",
        "key_id": key_id,
        "event_count": len(events),
        "operations": dict(operation_counts),
        "statuses": dict(status_counts),
        "events": [event.__dict__ for event in events],
    }
