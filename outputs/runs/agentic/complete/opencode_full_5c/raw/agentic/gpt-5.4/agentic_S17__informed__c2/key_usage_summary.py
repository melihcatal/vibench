from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional

from security_client import get_cloudtrail_client, get_kms_key_id
from security_models import KeyUsageSummary, normalize_event_list


KMS_EVENT_NAMES = [
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "Sign",
    "Verify",
]


def key_usage_summary(key_id: Optional[str] = None, max_results: int = 50) -> Dict[str, object]:
    resolved_key_id = get_kms_key_id(key_id)
    cloudtrail = get_cloudtrail_client()
    events: List[Dict[str, object]] = []
    for event_name in KMS_EVENT_NAMES:
        response = cloudtrail.lookup_events(
            LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": event_name}],
            MaxResults=max_results,
        )
        events.extend(response.get("Events", []))
    normalized = normalize_event_list(events)
    filtered = [
        event for event in normalized if resolved_key_id in str(event.get("CloudTrailEvent", "")) or resolved_key_id == event.get("Resources", [{}])[0].get("ResourceName") if event.get("Resources") else resolved_key_id in str(event)
    ]
    operation_counts = Counter(event.get("EventName", "unknown") for event in filtered)
    principals = {str(event.get("Username", "unknown")) for event in filtered}
    event_times = [str(event.get("EventTime")) for event in filtered if event.get("EventTime")]
    summary = KeyUsageSummary(
        provider="aws-cloudtrail",
        key_id=resolved_key_id,
        total_events=len(filtered),
        operations=dict(operation_counts),
        unique_principals=len(principals),
        earliest_event_time=min(event_times) if event_times else None,
        latest_event_time=max(event_times) if event_times else None,
    )
    return summary.to_dict()
