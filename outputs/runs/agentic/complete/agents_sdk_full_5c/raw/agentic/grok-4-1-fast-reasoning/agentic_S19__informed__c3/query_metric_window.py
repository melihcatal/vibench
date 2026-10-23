from observability_client import cloudwatch_client, get_time_window
from observability_models import extract_averages
from typing import List

def query_metric_window(metric_name: str, namespace: str = 'AWS/EC2', hours: float = 1.0) -> List[float]:
    start_time, end_time = get_time_window(hours)
    response = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    datapoints = response.get('Datapoints', [])
    return extract_averages(datapoints)