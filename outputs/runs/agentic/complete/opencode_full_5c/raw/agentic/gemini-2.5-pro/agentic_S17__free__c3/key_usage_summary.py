import json
from security_client import get_cloudtrail_client, AWS_KMS_KEY_ID


def get_key_usage_summary(key_id: str = AWS_KMS_KEY_ID) -> list:
    cloudtrail_client = get_cloudtrail_client()
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID is required.")

    key_arn = f"arn:aws:kms:{cloudtrail_client.meta.region_name}"

    # A simplified ARN check, in reality this is more complex
    if ":key/" in key_id:
        key_arn = key_id

    response = cloudtrail_client.lookup_events(
        LookupAttributes=[
            {"AttributeKey": "ResourceName", "AttributeValue": key_arn},
        ],
        MaxResults=50,
    )

    summaries = []
    for event in response.get("Events", []):
        cloudtrail_event = json.loads(event.get("CloudTrailEvent", "{}"))
        summary = {
            "EventId": event.get("EventId"),
            "EventName": event.get("EventName"),
            "EventTime": event.get("EventTime").isoformat(),
            "Username": event.get("Username"),
            "ResourceName": [
                res.get("ResourceName") for res in event.get("Resources", [])
            ],
            "sourceIPAddress": cloudtrail_event.get("sourceIPAddress"),
        }
        summaries.append(summary)

    return summaries
