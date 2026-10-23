import os
import datetime
import boto3

def aggregate_metric_stats(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int, # seconds
    statistics: list[str],
    dimensions: list[dict] = None
):
    """
    Retrieves aggregated statistics for a metric over a time window using Amazon CloudWatch.
    """
    client = boto3.client(
        'cloudwatch',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics,
        Dimensions=dimensions or []
    )
    return response

