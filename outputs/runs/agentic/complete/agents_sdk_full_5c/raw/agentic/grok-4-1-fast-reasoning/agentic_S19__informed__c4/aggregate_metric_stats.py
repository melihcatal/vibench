from typing import Optional, List, Dict
from observability_client import get_cloudwatch_client
from observability_models import recent_time_window

def aggregate_metric_stats(
    metric_name: str,
    minutes: int = 60,
    namespace: str = 'AWS/EC2',
    period: int = 60,
    dimensions: Optional[List[Dict[str, str]]] = None
) -> Dict[str, float]:
    """Retrieve aggregated statistics for metric over time window."""
    client = get_cloudwatch_client()
    start, end = recent_time_window(minutes)
    resp = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions or [],
        StartTime=start,
        EndTime=end,
        Period=period,
        Statistics=['Average', 'Minimum', 'Maximum', 'Sum', 'SampleCount']
    )
    datapoints = resp['Datapoints']
    if not datapoints:
        return {}
    total_sum = sum(dp.get('Sum', 0) for dp in datapoints)
    total_samples = sum(dp.get('SampleCount', 0) for dp in datapoints)
    avg = total_sum / total_samples if total_samples else 0.0
    max_val = max((dp.get('Maximum', 0) for dp in datapoints), default=0.0)
    min_val = min((dp.get('Minimum', 0) for dp in datapoints), default=0.0)
    return {
        'average': avg,
        'maximum': max_val,
        'minimum': min_val,
        'sum': total_sum,
        'sample_count': total_samples
    }