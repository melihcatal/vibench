from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from security_client import get_cloudtrail_client, get_kms_key_id
from security_models import KeyUsageSummary


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
) -> KeyUsageSummary:
    resolved_key_id = get_kms_key_id(key_id)
    client = get_cloudtrail_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=lookback_hours)

    paginator = client.get_paginator("lookup_events")
    events: List[Dict[str, str]] = []
    counts: Counter[str] = Counter()

    for page in paginator.paginate(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": resolved_key_id}],
        StartTime=start_time,
        EndTime=end_time,
    ):
        for event in page.get("Events", []):
            event_name = event.get("EventName", "")
            if event_name in KMS_EVENT_NAMES:
                counts[event_name] += 1
                events.append(
                    {
                        "event_id": event.get("EventId", ""),
                        "event_name": event_name,
                        "event_time": event.get("EventTime").isoformat() if event.get("EventTime") else "",
                        "username": event.get("Username", ""),
                    }
                )

    return KeyUsageSummary(
        key_id=resolved_key_id,
        cloudtrail_events=events,
        counts_by_event=dict(counts),
    )
