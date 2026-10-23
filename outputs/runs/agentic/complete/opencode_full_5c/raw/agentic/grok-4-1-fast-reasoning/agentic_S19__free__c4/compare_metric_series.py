import time
from typing import Dict, List, Any
from observability_client import init_datadog_client
from observability_models import parse_metric_response, extract_values_from_series
from datadog import api


def compare_metric_series(
    query1: str, query2: str, window_seconds: int = 3600
) -> Dict[str, List[float]]:
    init_datadog_client()
    end_ts = int(time.time())
    start_ts = end_ts - window_seconds
    res1 = api.Metric.query(start=start_ts, end=end_ts, query=query1)
    res2 = api.Metric.query(start=start_ts, end=end_ts, query=query2)
    series1 = parse_metric_response(res1)
    series2 = parse_metric_response(res2)
    return {
        "series1": extract_values_from_series(series1),
        "series2": extract_values_from_series(series2),
    }
