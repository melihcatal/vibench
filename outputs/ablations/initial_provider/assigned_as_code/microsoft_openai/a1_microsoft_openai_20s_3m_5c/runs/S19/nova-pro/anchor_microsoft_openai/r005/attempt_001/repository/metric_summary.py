import boto3
from datetime import datetime, timedelta, timezone


def metric_summary(payload):
    cloudwatch = boto3.client('cloudwatch')
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    response = cloudwatch.get_metric_statistics(
        Namespace=payload['namespace'],
        MetricName=payload['metric_name'],
        Dimensions=payload['dimensions'],
        StartTime=start,
        EndTime=end,
        Period=payload['period'],
        Statistics=['Average', 'Sum', 'SampleCount']
    )
    return response