from typing import List, Dict
from google.cloud import monitoring_v3
from observability_client import get_project_id
from observability_models import create_time_interval, build_metric_filter

def query_metric_window(metric_name: str, window_minutes: int = 60) -> List[Dict[str, float]]:
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
    datapoints: List[Dict[str, float]] = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            end_time = point.interval.end_time
            timestamp = end_time.seconds + (getattr(end_time, 'nanos', 0) / 1e9)
            value = getattr(point.value, 'double_value', 0.0) or getattr(point.value, 'int64_value', 0.0) or 0.0
            datapoints.append({"timestamp": timestamp, "value": float(value)})
    return sorted(datapoints, key=lambda p: p["timestamp"])
