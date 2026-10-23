import boto3


def key_usage_summary(region_name: str = "us-east-1") -> dict:
    cloudtrail = boto3.client("cloudtrail", region_name=region_name)
    events = cloudtrail.lookup_events(
        LookupAttributes=[
            {"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}
        ]
    )
    items = events.get("Events", [])
    return {
        "provider": "aws_kms",
        "event_count": len(items),
        "latest_event": items[0]["EventName"] if items else None,
    }
