import boto3
import os
from datetime import datetime
from typing import List
from observability_models import normalize_get_metric_statistics_datapoints

def aggregate_metric_stats(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    statistics: List[str] = None
) -> List[Dict]:
    if statistics is None:
        statistics = ['Average', 'Sum', 'SampleCount', 'Minimum', 'Maximum']
    client = boto3.client('cloudwatch', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics
    )
    return normalize_get_metric_statistics_datapoints(response['Datapoints'])
