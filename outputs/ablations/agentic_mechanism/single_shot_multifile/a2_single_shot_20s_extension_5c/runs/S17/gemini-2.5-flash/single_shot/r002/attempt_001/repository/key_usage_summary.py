import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import boto3
from security_client import get_cloudtrail_client
from security_models import KeyUsageEvent

def summarize_kms_key_usage(start_time: datetime, end_time: datetime, key_id: str = None) -> List[KeyUsageEvent]:
    """Summarizes AWS KMS key usage and crypto events using AWS CloudTrail."""
    cloudtrail_client = get_cloudtrail_client()

    if key_id is None:
        key_id = os.environ.get("KMS_KEY_ID")

    # CloudTrail lookup_events is limited by time range and max results
    # For comprehensive summaries, CloudTrail + S3 + Athena/CloudWatch Logs Insights is preferred
    # This function uses lookup_events for a simpler direct API call.

    events: List[KeyUsageEvent] = []
    try:
        paginator = cloudtrail_client.get_paginator('lookup_events')
        response_iterator = paginator.paginate(
            LookupAttributes=[
                {'AttributeKey': 'EventSource', 'AttributeValue': 'kms.amazonaws.com'},
                {'AttributeKey': 'ResourceName', 'AttributeValue': key_id} # Filter by key_id if provided
            ] if key_id else [
                {'AttributeKey': 'EventSource', 'AttributeValue': 'kms.amazonaws.com'}
            ],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=50 # CloudTrail lookup_events max results per call is 50
        )

        for page in response_iterator:
            for event_data in page.get('Events', []):
                # Minimal parsing for demonstration
                event_time_str = event_data.get('EventTime')
                event_datetime = datetime.fromtimestamp(int(event_time_str.timestamp())) if isinstance(event_time_str, datetime) else None

                # Basic structure, a more robust parser would handle nested JSON from CloudTrail logs
                event = KeyUsageEvent(
                    event_id=event_data.get('EventId', 'N/A'),
                    event_name=event_data.get('EventName', 'N/A'),
                    event_source=event_data.get('EventSource', 'N/A'),
                    event_time=event_datetime,
                    user_identity=event_data.get('CloudTrailEvent', {}), # For simplicity, storing raw event here
                    resources=event_data.get('Resources', [])
                )
                events.append(event)
    except Exception as e:
        raise RuntimeError(f"Failed to summarize key usage from CloudTrail: {e}")
    
    return events