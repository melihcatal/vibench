import boto3
from typing import List, Dict
from observability_client import parse_iso_time, get_default_region
from query_metric_window import query_metric_window

def filter_metric_dimensions(
    namespace: str,
    metric_name: str,
    dimensions: List[Dict[str, str]],
    start_time: str,
    end_time: str,
    period: int = 300
) -> List[Dict]:
    # Filter by providing dimensions
    return query_metric_window(
        namespace, metric_name, start_time, end_time, dimensions=dimensions, period=period
    )
