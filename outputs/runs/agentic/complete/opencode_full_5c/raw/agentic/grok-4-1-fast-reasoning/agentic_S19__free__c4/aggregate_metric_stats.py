import time
from typing import Dict, Any
from observability_client import init_datadog_client
from observability_models import (
    parse_metric_response,
    build_metric_query,
    extract_values_from_series,
    compute_stats,
)
from datadog import api


def aggregate_metric_stats(
    metric_name: str, window_seconds: int = 3600
) -> Dict[str, Any]:
    init_datadog_client()
    end_ts = int(time.time())
    start_ts = end_ts - window_seconds
    query_str = build_metric_query(metric_name)
    response = api.Metric.query(start=start_ts, end=end_ts, query=query_str)
    series = parse_metric_response(response)
    values = extract_values_from_series(series)
    return compute_stats(values)
