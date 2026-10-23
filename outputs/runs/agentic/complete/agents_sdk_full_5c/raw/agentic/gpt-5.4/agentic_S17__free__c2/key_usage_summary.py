from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional

from security_client import get_cloudtrail_client
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


def summarize_key_usage(lookup_value: Optional[str] = None, hours: int = 24) -> KeyUsageSummary:
    cloudtrail = get_cloudtrail_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    kwargs = {
        "StartTime": start_time,
        "EndTime": end_time,
        "MaxResults": 50,
    }
    if lookup_value:
        kwargs["LookupAttributes"] = [
            {"AttributeKey": "ResourceName", "AttributeValue": lookup_value}
        ]

    response = cloudtrail.lookup_events(**kwargs)
    events = [e for e in response.get("Events", []) if e.get("EventName") in KMS_EVENT_NAMES]

    key_names = _extract_resource_names(events)
    counts = Counter(event["EventName"] for event in events)
    return KeyUsageSummary(
        provider="aws-cloudtrail",
        events_found=len(events),
        keys=sorted(set(key_names)),
        by_event_name=dict(counts),
    )


def _extract_resource_names(events: Iterable[dict]) -> list[str]:
    names: list[str] = []
    for event in events:
        for resource in event.get("Resources", []):
            name = resource.get("ResourceName")
            if name:
                names.append(name)
    return names
