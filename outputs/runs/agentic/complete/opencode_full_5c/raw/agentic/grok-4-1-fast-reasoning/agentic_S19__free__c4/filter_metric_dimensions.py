import time
from typing import Dict, List, Any
from observability_client import init_datadog_client
from observability_models import parse_metric_response, build_metric_query
from datadog import api


def filter_metric_dimensions(
    metric_name: str, dimensions: Dict[str, str], window_seconds: int = 3600
) -> List[Dict[str, Any]]:
    init_datadog_client()
    end_ts = int(time.time())
    start_ts = end_ts - window_seconds
    query_str = build_metric_query(metric_name, dimensions)
    response = api.Metric.query(start=start_ts, end=end_ts, query=query_str)
    return parse_metric_response(response)
