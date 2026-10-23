import boto3


def key_usage_summary(key_id: str):
    client = boto3.client("cloudtrail")
    events = client.lookup_events(LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}])
    return {"provider": "aws-cloudtrail", "event_count": len(events.get("Events", [])), "key_id": key_id}
