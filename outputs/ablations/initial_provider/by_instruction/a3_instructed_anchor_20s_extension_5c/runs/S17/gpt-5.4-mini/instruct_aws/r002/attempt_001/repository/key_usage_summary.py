from __future__ import annotations

import boto3


def key_usage_summary(key_id: str) -> dict:
    cloudtrail = boto3.client("cloudtrail")
    response = cloudtrail.lookup_events(LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}])
    return {"provider": "aws", "key_id": key_id, "event_count": len(response.get("Events", [])), "events": [event.get("EventName") for event in response.get("Events", [])]}
