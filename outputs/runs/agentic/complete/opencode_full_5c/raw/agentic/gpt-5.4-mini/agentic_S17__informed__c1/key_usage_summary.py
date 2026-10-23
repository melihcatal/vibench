import boto3
from datetime import datetime, timedelta, timezone


def key_usage_summary(key_id, region=None, days=30):
    kms = boto3.client('kms', region_name=region or 'us-east-1')
    cloudtrail = boto3.client('cloudtrail', region_name=region or 'us-east-1')
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    events = cloudtrail.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName', 'AttributeValue': key_id}], StartTime=start, EndTime=end).get('Events', [])
    return {'key_id': key_id, 'event_count': len(events), 'latest_event': events[0]['EventName'] if events else None, 'provider': 'AWS KMS'}
