import boto3
from datetime import datetime, timedelta, timezone

def summarize_metric_trends(payload, config=None):
    config = config or {}
    cloudwatch = boto3.client('cloudwatch', region_name=config.get('region', 'us-west-2'))
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    response = cloudwatch.get_metric_statistics(
        Namespace=payload['namespace'],
        MetricName=payload['metric'],
        Dimensions=[{'Name': key, 'Value': value} for key, value in payload['dimensions'].items()],
        StartTime=start,
        EndTime=end,
        Period=config.get('period_seconds', 60),
        Statistics=['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum'])
    return response