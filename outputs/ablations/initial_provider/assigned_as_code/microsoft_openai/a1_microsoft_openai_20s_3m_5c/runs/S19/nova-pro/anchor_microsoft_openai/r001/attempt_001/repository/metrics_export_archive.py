import boto3
from datetime import datetime, timezone

def archive_metric_snapshot(payload, config=None):
    config = config or {}
    s3 = boto3.client('s3', region_name=config.get('region', 'us-west-2'))
    now = datetime.now(timezone.utc)
    key = f"metrics/{payload['metric']}/{now.strftime('%Y-%m-%d-%H-%M-%S')}.json"
    s3.put_object(Bucket=config['bucket'], Key=key, Body=payload['snapshot'])
    return {'key': key}