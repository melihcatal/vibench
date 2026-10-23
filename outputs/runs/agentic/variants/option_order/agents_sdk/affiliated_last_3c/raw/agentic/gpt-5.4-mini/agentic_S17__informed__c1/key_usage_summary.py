from __future__ import annotations

import boto3


def key_usage_summary(key_id: str, region_name: str | None = None) -> dict:
    client = boto3.client("cloudtrail", region_name=region_name)
    response = client.lookup_events(LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}])
    events = response.get("Events", [])
    summary = {"provider": "AWS CloudTrail", "key_id": key_id, "event_count": len(events), "events": []}
    for event in events:
        summary["events"].append({"event_name": event.get("EventName"), "event_time": event.get("EventTime").isoformat() if event.get("EventTime") else None})
    return summary
