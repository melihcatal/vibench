from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Optional

from security_client import cloudtrail_client
from security_models import KeyUsageSummary


KMS_EVENT_NAMES = {
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "Sign",
    "Verify",
    "ReEncrypt",
}



def key_usage_summary(lookup_attribute_value: Optional[str] = None, max_results: int = 25) -> KeyUsageSummary:
    client = cloudtrail_client()
    lookup_attributes: List[Dict[str, str]] = []
    if lookup_attribute_value:
        lookup_attributes.append({"AttributeKey": "ResourceName", "AttributeValue": lookup_attribute_value})

    response = client.lookup_events(LookupAttributes=lookup_attributes, MaxResults=max_results)
    events = response.get("Events", [])
    filtered = [event for event in events if event.get("EventName") in KMS_EVENT_NAMES]
    counts = Counter(event.get("EventName", "Unknown") for event in filtered)

    recent_events: List[Dict[str, Any]] = [
        {
            "event_name": event.get("EventName"),
            "event_time": event.get("EventTime").isoformat() if event.get("EventTime") else None,
            "username": event.get("Username"),
            "event_id": event.get("EventId"),
        }
        for event in filtered
    ]

    return KeyUsageSummary(
        provider="aws-cloudtrail",
        total_events=len(filtered),
        operation_counts=dict(counts),
        recent_events=recent_events,
    )
