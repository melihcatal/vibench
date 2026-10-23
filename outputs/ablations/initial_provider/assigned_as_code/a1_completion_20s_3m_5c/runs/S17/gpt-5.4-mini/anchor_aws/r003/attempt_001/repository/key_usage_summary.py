import boto3


def key_usage_summary(payload, config=None):
    config = config or {}
    cloudtrail = boto3.client("cloudtrail", region_name=config.get("region"))
    events = cloudtrail.lookup_events(MaxResults=10).get("Events", [])
    return {"event_count": len(events), "latest_event_names": [event.get("EventName") for event in events]}
