import boto3
import os
from datetime import datetime, timedelta

def aggregate_metric_stats(metric_name: str, namespace: str, start_time: datetime, end_time: datetime, period: int, statistic: str, dimensions: list = None):
    """
    Retrieves aggregated statistics for a metric over a time window using AWS CloudWatch.

    Args:
        metric_name: The name of the metric.
        namespace: The namespace of the metric.
        start_time: The start time for the query.
        end_time: The end time for the query.
        period: The granularity, in seconds, of the returned data points.
        statistic: The statistic to apply to the metric data. e.g., 'Average', 'Sum', 'Maximum', 'Minimum', 'SampleCount'.
        dimensions: A list of dictionaries representing metric dimensions.
                    Example: [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]
    """
    cloudwatch = boto3.client(
        'cloudwatch',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions if dimensions is not None else [],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic]
    )
    return response.get('Datapoints', [])

