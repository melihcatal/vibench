import boto3
import os
from datetime import datetime, timedelta

def filter_metric_dimensions(metric_name: str, namespace: str, start_time: datetime, end_time: datetime, period: int, dimensions: list):
    """
    Queries metric data filtered by resource labels or dimensions using AWS CloudWatch.

    Args:
        metric_name: The name of the metric.
        namespace: The namespace of the metric.
        start_time: The start time for the query.
        end_time: The end time for the query.
        period: The granularity, in seconds, of the returned data points.
        dimensions: A list of dictionaries representing metric dimensions to filter by.
                    Example: [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]
    """
    cloudwatch = boto3.client(
        'cloudwatch',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    metric_query = {
        'Id': 'm1',
        'MetricStat': {
            'Metric': {
                'Namespace': namespace,
                'MetricName': metric_name,
                'Dimensions': dimensions
            },
            'Period': period,
            'Stat': 'Average' # Can be adjusted based on requirement
        },
        'ReturnData': True
    }

    response = cloudwatch.get_metric_data(
        MetricDataQueries=[metric_query],
        StartTime=start_time,
        EndTime=end_time,
        ScanBy='TimestampAscending'
    )
    return response.get('MetricDataResults', [])

