from __future__ import annotations

from datetime import datetime, timedelta, timezone

from security_client import aws_account_id, aws_region, cloudtrail_client
from security_models import KeyUsageSummary


def key_usage_summary(key_id: str, hours: int = 24) -> KeyUsageSummary:
    client = cloudtrail_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    resource_name = (
        key_id
        if key_id.startswith("arn:aws:kms:")
        else f"arn:aws:kms:{aws_region()}:{aws_account_id()}:key/{key_id}"
    )
    response = client.lookup_events(
        LookupAttributes=[
            {"AttributeKey": "ResourceName", "AttributeValue": resource_name}
        ],
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=50,
    )
    events = response.get("Events", [])
    counts: dict[str, int] = {}
    for event in events:
        name = event.get("EventName", "Unknown")
        counts[name] = counts.get(name, 0) + 1
    summary = (
        ", ".join(f"{name}:{count}" for name, count in sorted(counts.items()))
        or "no-events"
    )
    return KeyUsageSummary(summary=summary, raw_events=events)
