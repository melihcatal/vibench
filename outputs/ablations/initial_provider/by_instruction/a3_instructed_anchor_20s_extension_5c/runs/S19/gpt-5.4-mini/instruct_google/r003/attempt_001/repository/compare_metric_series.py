from datetime import datetime, timedelta, timezone

from observability_client import GoogleCloudMonitoringClient


def compare_metric_series(metric_name: str, left_filter: str, right_filter: str, minutes: int = 60):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    client = GoogleCloudMonitoringClient()
    left = client.list_time_series(metric_name, start_time, end_time, filter_expr=left_filter)
    right = client.list_time_series(metric_name, start_time, end_time, filter_expr=right_filter)
    return {"left": [p.value for p in left.points], "right": [p.value for p in right.points]}
