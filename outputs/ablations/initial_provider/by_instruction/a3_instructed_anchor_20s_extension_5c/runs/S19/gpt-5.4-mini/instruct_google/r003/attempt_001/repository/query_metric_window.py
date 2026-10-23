from datetime import datetime, timedelta, timezone

from observability_client import GoogleCloudMonitoringClient


def query_metric_window(metric_name: str, minutes: int = 60, filter_expr: str | None = None):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    client = GoogleCloudMonitoringClient()
    return client.list_time_series(metric_name, start_time, end_time, filter_expr=filter_expr)
