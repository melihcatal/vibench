
import boto3
import datetime
from typing import List, Dict

def get_key_usage_summary_from_cloudtrail(key_id: str, days: int = 7) -> List[Dict]:
    """
    Summarizes usage for a specific AWS KMS key by querying CloudTrail.
    
    Note: CloudTrail must be configured to log KMS management and data events.
    """
    client = boto3.client('cloudtrail')
    
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(days=days)

    events = []
    paginator = client.get_paginator('lookup_events')
    
    pages = paginator.paginate(
        LookupAttributes=[
            {
                'AttributeKey': 'ResourceName',
                'AttributeValue': key_id
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=50
    )

    for page in pages:
        for event in page.get('Events', []):
            summary = {
                "EventId": event.get("EventId"),
                "EventName": event.get("EventName"),
                "EventTime": event.get("EventTime").isoformat(),
                "Username": event.get("Username"),
                "ReadOnly": event.get("ReadOnly"),
                "EventSource": event.get("EventSource"),
            }
            events.append(summary)
            
    return events
