import boto3
import statistics
from typing import List, Dict, Optional
from observability_client import parse_iso_time, get_default_region
from query_metric_window import query_metric_window

def aggregate_metric_stats(
    namespace: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    dimensions: Optional[List[Dict[str, str]]] = None,
    period: int = 60
) -> Dict[str, float]:
    datapoints = query_metric_window(
        namespace, metric_name, start_time, end_time, dimensions, period, ['Average']
    )
    if not datapoints:
        return {}
    avgs = [dp['Average'] for dp in datapoints]
    return {
        'min': min(avgs),
        'max': max(avgs),
        'mean': statistics.mean(avgs),
        'stddev': statistics.stdev(avgs) if len(avgs) > 1 else 0.0
    }
