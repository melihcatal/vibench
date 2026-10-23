import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from security_client import get_cloudtrail_client
from security_models import KeyUsageEvent

def summarize_key_usage(
    start_time: datetime,
    end_time: datetime,
    event_name_prefix: str = 'Encrypt', # Common KMS events start with Encrypt, Decrypt, GenerateDataKey, Sign, Verify
    region: str = 'us-east-1'
) -> List[KeyUsageEvent]:
    """
    Summarizes key usage and crypto events using AWS CloudTrail lookup events.
    Filters events related to KMS key usage.
    """
    cloudtrail_client = get_cloudtrail_client(region)
    
    events: List[KeyUsageEvent] = []
    
    paginator = cloudtrail_client.get_paginator('lookup_events')
    pages = paginator.paginate(
        LookupAttributes=[
            {'AttributeKey': 'EventSource', 'AttributeValue': 'kms.amazonaws.com'}
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    for page in pages:
        for event_data in page.get('Events', []):
            event_name = event_data.get('EventName')
            if event_name and event_name.startswith(event_name_prefix):
                cloudtrail_event = json.loads(event_data['CloudTrailEvent'])
                
                key_arn = "N/A"
                if 'requestParameters' in cloudtrail_event and 'keyId' in cloudtrail_event['requestParameters']:
                    key_arn = cloudtrail_event['requestParameters']['keyId']
                elif 'resources' in cloudtrail_event:
                    for resource in cloudtrail_event['resources']:
                        if resource.get('resourceType') == 'AWS::KMS::Key':
                            key_arn = resource.get('resourceName', "N/A")
                            break
                
                user_identity = cloudtrail_event.get('userIdentity', {})
                
                events.append(
                    KeyUsageEvent(
                        event_id=event_data.get('EventId'),
                        event_name=event_name,
                        event_time=event_data.get('EventTime').isoformat(),
                        key_arn=key_arn,
                        user_identity=user_identity
                    )
                )
    return events

if __name__ == '__main__':
    # This is example usage and should not be part of the final submission.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set in environment variables.
    
    # end_time = datetime.now()
    # start_time = end_time - timedelta(days=7) # Look back 7 days
    
    # usage_summary = summarize_key_usage(start_time, end_time)
    # for event in usage_summary:
    #     print(f"Event ID: {event.event_id}, Name: {event.event_name}, Key ARN: {event.key_arn}")
