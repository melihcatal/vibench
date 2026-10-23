import boto3
from datetime import datetime
from typing import List, Dict
from observability_client import get_cloudwatch_client
from observability_models import MetricDatapoint

def aggregate_metric_stats(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    statistics: List[str] = ['Average', 'Sum', 'Minimum', 'Maximum'],
    namespace: str = 'AWS/EC2',
    period: int = 300,
    region: str = None
) -> Dict[str, List[MetricDatapoint]]:
    client = get_cloudwatch_client(region)
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics
    )
    stats_data = {stat: [] for stat in statistics}
    for dp in response['Datapoints']:
        timestamp = dp['Timestamp']
        for stat in statistics:
            value = dp.get(stat)
            if value is not None:
                stats_data[stat].append(MetricDatapoint(timestamp=timestamp, value=value))
    return stats_data
