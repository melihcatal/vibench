from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from security_client import cloudtrail_client
from security_models import KeyUsageSummary


KMS_EVENT_NAMES = {"Encrypt", "Decrypt", "GenerateDataKey", "Sign", "Verify", "ReEncrypt", "GenerateDataKeyWithoutPlaintext"}


def key_usage_summary(key_id: str, hours: int = 24, region_name: str | None = None) -> KeyUsageSummary:
    client = cloudtrail_client(region_name)
    start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    paginator = client.get_paginator("lookup_events")

    recent_events: List[Dict[str, Any]] = []
    actions: Counter[str] = Counter()

    for page in paginator.paginate(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}],
        StartTime=start_time,
        EndTime=datetime.now(timezone.utc),
    ):
        for event in page.get("Events", []):
            event_name = event.get("EventName", "")
            if event_name not in KMS_EVENT_NAMES:
                continue
            actions[event_name] += 1
            recent_events.append(
                {
                    "event_id": event.get("EventId"),
                    "event_name": event_name,
                    "username": event.get("Username"),
                    "event_time": event.get("EventTime").isoformat() if event.get("EventTime") else None,
                    "cloudtrail_event": event.get("CloudTrailEvent"),
                }
            )

    return KeyUsageSummary(
        key_id=key_id,
        total_events=sum(actions.values()),
        actions=dict(actions),
        recent_events=recent_events,
        provider="aws-cloudtrail",
    )
