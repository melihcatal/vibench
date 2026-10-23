import boto3


def key_usage_summary(payload, config=None):
    config = config or {}
    client = boto3.client("cloudtrail", region_name=config.get("region"))
    response = client.lookup_events(LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": "Encrypt"}])
    return {"events": response.get("Events", []), "payload": payload}
