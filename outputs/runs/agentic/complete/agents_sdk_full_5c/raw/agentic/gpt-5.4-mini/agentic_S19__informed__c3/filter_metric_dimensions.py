from __future__ import annotations

from observability_client import ObservabilityClient
from observability_models import infer_time_window


def filter_metric_dimensions(metric_name: str, labels: dict[str, str], minutes: int = 60, statistic: str = "Average"):
    start_time, end_time = infer_time_window(minutes)
    client = ObservabilityClient()
    return client.query_series(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=labels, statistic=statistic)
