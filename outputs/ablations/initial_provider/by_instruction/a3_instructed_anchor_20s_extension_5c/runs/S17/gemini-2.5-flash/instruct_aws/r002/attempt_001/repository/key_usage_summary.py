import os
import boto3
from datetime import datetime, timedelta
from typing import List, Dict, Any

def summarize_key_usage(lookup_attribute_key: str = 'EventName', lookup_attribute_value: str = 'Encrypt', hours_ago: int = 24) -> List[Dict[str, Any]]:
    cloudtrail_client = boto3.client('cloudtrail', region_name=os.environ.get("AWS_REGION", "us-east-1"))
    start_time = datetime.now() - timedelta(hours=hours_ago)

    events = []
    paginator = cloudtrail_client.get_paginator('lookup_events')
    response_iterator = paginator.paginate(
        LookupAttributes=[
            {
                'AttributeKey': lookup_attribute_key,
                'AttributeValue': lookup_attribute_value
            },
        ],
        StartTime=start_time,
    )

    for page in response_iterator:
        for event in page['Events']:
            events.append({
                'EventId': event['EventId'],
                'EventName': event['EventName'],
                'Username': event['Username'],
                'EventTime': event['EventTime'].isoformat()
            })
    return events
