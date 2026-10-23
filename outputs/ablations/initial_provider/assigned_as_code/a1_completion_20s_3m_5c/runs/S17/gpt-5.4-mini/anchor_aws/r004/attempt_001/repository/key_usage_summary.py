import boto3


def key_usage_summary(payload=None, config=None):
    config = config or {}
    client = boto3.client("cloudtrail", region_name=config.get("region"))
    response = client.lookup_events(LookupAttributes=[{"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}])
    events = response.get("Events", [])
    return {"event_count": len(events), "latest_event": events[0]["EventName"] if events else None}
