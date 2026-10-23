from observability_client import cloudwatch_client, get_time_window
from observability_models import extract_averages
from typing import Dict

def aggregate_metric_stats(metric_name: str, namespace: str = 'AWS/EC2', hours: float = 1.0) -> Dict[str, float]:
    start_time, end_time = get_time_window(hours)
    response = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average', 'Minimum', 'Maximum', 'Sum', 'SampleCount']
    )
    datapoints = response.get('Datapoints', [])
    if not datapoints:
        return {}
    avgs = extract_averages(datapoints)
    mins = [dp.get('Minimum', 0.0) for dp in datapoints]
    maxs = [dp.get('Maximum', 0.0) for dp in datapoints]
    sums = [dp.get('Sum', 0.0) for dp in datapoints]
    counts = [dp.get('SampleCount', 0.0) for dp in datapoints]
    return {
        'avg': sum(avgs) / len(avgs),
        'min': min(mins),
        'max': max(maxs),
        'total_sum': sum(sums),
        'total_count': sum(counts),
    }