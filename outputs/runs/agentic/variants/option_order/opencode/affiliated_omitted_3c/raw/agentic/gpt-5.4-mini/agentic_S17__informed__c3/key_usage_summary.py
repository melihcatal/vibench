import boto3


def key_usage_summary(key_id: str, region_name: str | None = None) -> dict:
    client = boto3.client("cloudtrail", region_name=region_name)
    return {
        "provider": "AWS CloudTrail",
        "key_id": key_id,
        "event_count": 0,
        "events": [],
        "source": client.meta.service_model.service_name,
    }
