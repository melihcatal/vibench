import os
import boto3
from datetime import datetime
from typing import List, Dict


def key_usage_summary(key_id: str, start_time: str, end_time: str) -> List[Dict]:
    """
    Summarizes AWS KMS key usage and crypto events.

    Args:
        key_id: AWS KMS key ID or ARN.
        start_time: Start time in ISO 8601 format.
        end_time: End time in ISO 8601 format.

    Returns:
        List of dictionaries containing key usage events.
    """
    client = boto3.client(
        "cloudtrail",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    response = client.lookup_events(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": key_id}],
        StartTime=datetime.fromisoformat(start_time),
        EndTime=datetime.fromisoformat(end_time),
    )

    events = []
    for event in response["Events"]:
        events.append(
            {
                "event_time": event["EventTime"].isoformat(),
                "event_name": event["EventName"],
                "event_source": event["EventSource"],
                "username": event.get("Username", "Unknown"),
                "resources": [
                    {
                        "resource_name": r["ResourceName"],
                        "resource_type": r["ResourceType"],
                    }
                    for r in event.get("Resources", [])
                ],
            }
        )

    return events
