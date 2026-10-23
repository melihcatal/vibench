from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional
import json

from security_client import AWS_KMS_PROVIDER, get_cloudtrail_client
from security_models import KeyUsageSummary


def key_usage_summary(
    key_id: str,
    start_time,
    end_time,
    region_name: Optional[str] = None,
) -> Dict[str, object]:
    client = get_cloudtrail_client(region_name)
    paginator = client.get_paginator("lookup_events")
    page_iterator = paginator.paginate(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}],
        StartTime=start_time,
        EndTime=end_time,
    )
    operation_counts: Counter = Counter()
    principals = set()
    timestamps: List[str] = []
    event_count = 0
    for page in page_iterator:
        for event in page.get("Events", []):
            event_count += 1
            operation_counts[event.get("EventName", "Unknown")] += 1
            timestamps.append(event["EventTime"].isoformat())
            raw_event = json.loads(event.get("CloudTrailEvent", "{}"))
            principal = raw_event.get("userIdentity", {}).get("arn") or raw_event.get(
                "userIdentity", {}
            ).get("principalId")
            if principal:
                principals.add(principal)
    summary = KeyUsageSummary(
        provider=AWS_KMS_PROVIDER,
        key_id=key_id,
        event_count=event_count,
        operation_counts=dict(operation_counts),
        principals=sorted(principals),
        first_seen=min(timestamps) if timestamps else None,
        last_seen=max(timestamps) if timestamps else None,
    )
    return summary.to_dict()
