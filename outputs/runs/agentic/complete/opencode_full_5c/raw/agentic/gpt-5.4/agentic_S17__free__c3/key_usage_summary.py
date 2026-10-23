from __future__ import annotations

from datetime import datetime, timedelta, timezone

from security_client import AWS_KMS_PROVIDER, get_cloudtrail_client
from security_models import KeyUsageSummary


def key_usage_summary(
    key_name: str, hours_back: int = 24, region_name: str | None = None
) -> KeyUsageSummary:
    cloudtrail = get_cloudtrail_client(region_name)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_back)
    response = cloudtrail.lookup_events(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_name}],
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=50,
    )
    events = response.get("Events", [])
    event_names = [event["EventName"] for event in events]
    return KeyUsageSummary(
        provider=AWS_KMS_PROVIDER,
        key_name=key_name,
        event_count=len(events),
        event_names=event_names,
        raw_events=events,
    )
