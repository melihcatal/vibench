from datetime import datetime, timedelta, timezone

from observability_client import GoogleCloudMonitoringClient


def filter_metric_dimensions(metric_name: str, dimensions: dict[str, str], minutes: int = 60):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    filter_expr = " AND ".join([f'metric.labels.{k} = "{v}"' for k, v in dimensions.items()])
    client = GoogleCloudMonitoringClient()
    return client.list_time_series(metric_name, start_time, end_time, filter_expr=filter_expr)
