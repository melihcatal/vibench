from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from security_client import cloudtrail_client
from security_models import UsageSummary


KMS_EVENT_NAMES = {
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "ReEncrypt",
    "Sign",
    "Verify",
}



def key_usage_summary(start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, key_arn_contains: Optional[str] = None) -> UsageSummary:
    client = cloudtrail_client()
    lookup_attributes = [{"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}]
    paginator = client.get_paginator("lookup_events")
    operations: Counter[str] = Counter()
    event_count = 0
    notes: List[str] = []
    for page in paginator.paginate(LookupAttributes=lookup_attributes, StartTime=start_time, EndTime=end_time):
        for event in page.get("Events", []):
            event_name = event.get("EventName")
            if event_name not in KMS_EVENT_NAMES:
                continue
            resources = event.get("Resources", [])
            if key_arn_contains and not any(key_arn_contains in (res.get("ResourceName") or "") for res in resources):
                continue
            operations[event_name] += 1
            event_count += 1
    notes.append("Source: AWS CloudTrail lookup_events for kms.amazonaws.com")
    return UsageSummary(
        provider="aws-cloudtrail",
        window_start=start_time.astimezone(timezone.utc).isoformat() if start_time else None,
        window_end=end_time.astimezone(timezone.utc).isoformat() if end_time else None,
        event_count=event_count,
        operations=dict(operations),
        notes=notes,
    )



def key_usage_summary_dict(start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, key_arn_contains: Optional[str] = None) -> Dict[str, Any]:
    result = key_usage_summary(start_time=start_time, end_time=end_time, key_arn_contains=key_arn_contains)
    return {
        "provider": result.provider,
        "window_start": result.window_start,
        "window_end": result.window_end,
        "event_count": result.event_count,
        "operations": result.operations,
        "notes": result.notes,
    }
