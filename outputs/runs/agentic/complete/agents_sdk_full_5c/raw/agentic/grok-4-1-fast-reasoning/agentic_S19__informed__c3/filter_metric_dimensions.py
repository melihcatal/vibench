from observability_client import cloudwatch_client, get_time_window
from observability_models import extract_averages
from typing import List, Dict, Any

def filter_metric_dimensions(metric_name: str, dimensions: List[Dict[str, str]], namespace: str = 'AWS/EC2', hours: float = 1.0) -> List[float]:
    start_time, end_time = get_time_window(hours)
    response = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    datapoints = response.get('Datapoints', [])
    return extract_averages(datapoints)