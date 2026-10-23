from typing import Dict, Any
from google.cloud import monitoring_v3
from observability_client import get_project_id
from observability_models import create_time_interval, build_metric_filter

def compare_metric_series(metric_name: str, dimensions_a: Dict[str, str], dimensions_b: Dict[str, str], window_minutes: int = 60) -> Dict[str, float]:
    client = monitoring_v3.MetricServiceClient()
    project_id = get_project_id()
    interval = create_time_interval(window_minutes)
    filter_a = build_metric_filter(metric_name, dimensions_a)
    filter_b = build_metric_filter(metric_name, dimensions_b)
    request_a = {
        "name": f"projects/{project_id}",
        "filter": filter_a,
        "interval": interval,
        "view": "FULL",
    }
    request_b = {
        "name": f"projects/{project_id}",
        "filter": filter_b,
        "interval": interval,
        "view": "FULL",
    }
    values_a: list[float] = []
    for time_series in client.list_time_series(request_a):
        for point in time_series.points:
            value = getattr(point.value, 'double_value', 0.0) or getattr(point.value, 'int64_value', 0.0) or 0.0
            values_a.append(float(value))
    values_b: list[float] = []
    for time_series in client.list_time_series(request_b):
        for point in time_series.points:
            value = getattr(point.value, 'double_value', 0.0) or getattr(point.value, 'int64_value', 0.0) or 0.0
            values_b.append(float(value))
    mean_a = sum(values_a) / len(values_a) if values_a else 0.0
    mean_b = sum(values_b) / len(values_b) if values_b else 0.0
    ratio = mean_a / mean_b if mean_b != 0 else float('inf')
    return {
        "mean_a": mean_a,
        "mean_b": mean_b,
        "diff": mean_a - mean_b,
        "ratio": ratio
    }
