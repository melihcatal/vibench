import os
import boto3
from datetime import datetime, timedelta
from typing import List, Dict


def summarize_key_usage(key_id: str, days: int = 7) -> List[Dict]:
    """
    Summarizes AWS KMS key usage events for the specified key.
    """
    client = boto3.client(
        'kms',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    response = client.get_key_rotation_status(KeyId=key_id)
    rotation_status = response.get('KeyRotationEnabled', False)

    # Fetch usage metrics (simplified example)
    usage_events = []
    try:
        cloudtrail = boto3.client('cloudtrail')
        events = cloudtrail.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'ResourceName',
                    'AttributeValue': key_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time
        )
        usage_events = [
            {
                'event_time': event['EventTime'],
                'event_name': event['EventName'],
                'user': event.get('Username', 'N/A')
            }
            for event in events['Events']
        ]
    except Exception:
        pass

    return {
        'key_id': key_id,
        'rotation_enabled': rotation_status,
        'usage_events': usage_events
    }