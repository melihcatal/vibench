import os

import boto3


def key_usage_summary(key_id: str = None):
    client = boto3.client("cloudtrail")
    trail_name = os.getenv("AWS_CLOUDTRAIL_NAME", "default")
    events = client.lookup_events(
        LookupAttributes=[
            {"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}
        ]
    )
    return {
        "trail": trail_name,
        "key_id": key_id or os.getenv("AWS_KMS_KEY_ID", "alias/app-key"),
        "event_count": len(events.get("Events", [])),
    }
