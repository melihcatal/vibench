import datetime
import statistics
from google.cloud import monitoring_v3
from .observability_client import query_time_series
from .observability_models import MetricQuery, TimeInterval

def aggregate_metric_stats(metric_name: str, duration_hours: int = 1) -> dict[str, float]:
    values = query_metric_window(metric_name, duration_hours)
    if not values:
        return {}
    return {
        "mean": statistics.mean(values),
        "max": max(values),
        "min": min(values),
        "stddev": statistics.stdev(values) if len(values) > 1 else 0.0
    }