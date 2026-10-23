from typing import Dict, List
from google.cloud import monitoring_v3
from observability_client import get_project_id
from observability_models import create_time_interval, build_metric_filter

def aggregate_metric_stats(metric_name: str, window_minutes: int = 60) -> Dict[str, float]:
    client = monitoring_v3.MetricServiceClient()
    project_id = get_project_id()
    interval = create_time_interval(window_minutes)
    filter_str = build_metric_filter(metric_name)
    request = {
        "name": f"projects/{project_id}",
        "filter": filter_str,
        "interval": interval,
        "view": "FULL",
    }
    values: List[float] = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            value = getattr(point.value, 'double_value', 0.0) or getattr(point.value, 'int64_value', 0.0) or 0.0
            values.append(float(value))
    if not values:
        return {}
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return {
        "min": min(values),
        "max": max(values),
        "mean": mean,
        "std": variance ** 0.5,
        "count": len(values)
    }
