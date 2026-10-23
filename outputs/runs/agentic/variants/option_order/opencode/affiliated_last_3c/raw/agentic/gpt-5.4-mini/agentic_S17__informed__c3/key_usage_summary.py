import os

import boto3


def key_usage_summary(key_id: str) -> dict:
    client = boto3.client(
        "cloudtrail", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    response = client.lookup_events(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}]
    )
    events = response.get("Events", [])
    return {
        "provider": "aws-cloudtrail",
        "key_id": key_id,
        "event_count": len(events),
        "event_names": [event.get("EventName") for event in events],
    }
