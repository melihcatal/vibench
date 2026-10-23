import boto3
from typing import List
from datetime import timezone
from observability_client import get_recent_time_window, normalize_cloudwatch_datapoints
from observability_models import MetricDatapoint

def query_metric_window(
    namespace: str,
    metric_name: str,
    duration_minutes: int = 60,
    period: int = 300
) -> List[MetricDatapoint]:
    client = boto3.client('cloudwatch')
    start_time, end_time = get_recent_time_window(duration_minutes)
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average'],
    )
    return normalize_cloudwatch_datapoints(response.get('Datapoints', []))