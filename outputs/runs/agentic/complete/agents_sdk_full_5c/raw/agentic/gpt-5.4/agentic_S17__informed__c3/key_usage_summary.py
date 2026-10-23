from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from security_client import get_cloudtrail_client
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



def key_usage_summary(
    key_id: Optional[str] = None,
    lookback_hours: int = 24,
    region_name: Optional[str] = None,
) -> UsageSummary:
    cloudtrail = get_cloudtrail_client(region_name=region_name)
    start_time = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    paginator = cloudtrail.get_paginator("lookup_events")
    pages = paginator.paginate(
        LookupAttributes=[{"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}],
        StartTime=start_time,
        EndTime=datetime.now(timezone.utc),
    )

    actions: Counter[str] = Counter()
    matched_events: List[Dict[str, Any]] = []
    for page in pages:
        for event in page.get("Events", []):
            event_name = event.get("EventName")
            resources = event.get("Resources", [])
            if event_name not in KMS_EVENT_NAMES:
                continue
            if key_id and not any(key_id in (r.get("ResourceName") or "") for r in resources):
                continue
            actions[event_name] += 1
            matched_events.append(event)

    return UsageSummary(
        key_id=key_id,
        event_count=len(matched_events),
        actions=dict(actions),
        provider="aws-cloudtrail",
        source="kms.amazonaws.com",
    )
