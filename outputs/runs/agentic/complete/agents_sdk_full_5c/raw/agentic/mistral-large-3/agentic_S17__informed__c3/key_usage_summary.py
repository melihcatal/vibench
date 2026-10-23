import boto3
from datetime import datetime, timedelta
from typing import Dict, List


def summarize_key_usage(key_id: str, days: int = 7) -> Dict[str, Any]:
    """
    Summarizes AWS KMS key usage and crypto events over a specified period.
    
    Args:
        key_id: The AWS KMS key ID or ARN.
        days: Number of days to look back.
    
    Returns:
        A dictionary containing key usage summary.
    """
    client = boto3.client("kms")
    cloudtrail = boto3.client("cloudtrail")
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    
    # Get key details
    key_details = client.describe_key(KeyId=key_id)
    
    # Query CloudTrail for KMS events
    events = []
    paginator = cloudtrail.get_paginator("lookup_events")
    for page in paginator.paginate(
        LookupAttributes=[
            {
                "AttributeKey": "EventSource",
                "AttributeValue": "kms.amazonaws.com"
            },
            {
                "AttributeKey": "ResourceName",
                "AttributeValue": key_id
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    ):
        events.extend(page["Events"])
    
    # Count operations
    operation_counts = {}
    for event in events:
        event_name = event["EventName"]
        operation_counts[event_name] = operation_counts.get(event_name, 0) + 1
    
    return {
        "key_id": key_id,
        "key_description": key_details["KeyMetadata"].get("Description", ""),
        "key_state": key_details["KeyMetadata"]["KeyState"],
        "operation_counts": operation_counts,
        "event_window_days": days,
        "provider": "aws_kms"
    }