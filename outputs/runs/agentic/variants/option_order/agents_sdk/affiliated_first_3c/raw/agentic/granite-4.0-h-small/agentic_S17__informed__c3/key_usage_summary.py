import os
import boto3
from datetime import datetime, timedelta
from security_client import kms_client

def key_usage_summary(key_id: str, start_date: datetime) -> dict:
    """Summarize AWS KMS key usage events since start_date using CloudTrail.",
    # Pull the last 7 days of CloudTrail events for KMS
    # Note: This example assumes CloudTrail log file lookup is configured.
    client = boto3.client('cloudtrail')
    end_time = datetime.utcnow()
    lookback = 7 * 24 * 60 * 60  # 7 days
    response = client.lookup_events(
        LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'Decrypt'}],
        StartTime=start_date,
        EndTime=end_time,
        MaxResults=20
    )
    events = response.get('Events', [])
    summary = {
        'key_id': key_id,
        'period_start': start_date.isoformat(),
        'period_end': end_time.isoformat(),
        'decrypt_calls': len(events),
        'events_sample': [e['EventName'] for e in events]
    }
    return summary
