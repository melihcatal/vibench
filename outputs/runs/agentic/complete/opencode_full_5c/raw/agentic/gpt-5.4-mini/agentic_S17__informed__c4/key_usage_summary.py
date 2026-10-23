import boto3


def key_usage_summary(key_id: str) -> dict:
    client = boto3.client("cloudtrail")
    events = client.lookup_events(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}]
    )
    return {
        "key_id": key_id,
        "event_count": len(events.get("Events", [])),
        "provider": "AWS CloudTrail",
    }
