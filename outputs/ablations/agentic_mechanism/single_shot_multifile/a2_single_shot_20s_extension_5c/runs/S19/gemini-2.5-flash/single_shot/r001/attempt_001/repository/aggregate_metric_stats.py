import os
import boto3
from datetime import datetime, timedelta

def aggregate_metric_stats(namespace: str, metric_name: str, statistic: str, period_seconds: int, minutes_ago: int = 60, dimensions: dict = None) -> list:
    cloudwatch = boto3.client(
        'cloudwatch',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes_ago)

    cw_dimensions = []
    if dimensions:
        for name, value in dimensions.items():
            cw_dimensions.append({'Name': name, 'Value': value})

    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period_seconds,
        Statistics=[statistic],
        Dimensions=cw_dimensions
    )

    datapoints = []
    for dp in response.get('Datapoints', []):
        datapoints.append({
            "timestamp": dp['Timestamp'].isoformat(),
            "value": dp[statistic],
            "unit": dp.get('Unit')
        })
    return datapoints