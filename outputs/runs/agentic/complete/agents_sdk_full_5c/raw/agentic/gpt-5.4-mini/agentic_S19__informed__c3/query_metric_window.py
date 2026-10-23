from __future__ import annotations

from datetime import timedelta

from observability_client import ObservabilityClient
from observability_models import MetricWindow, infer_time_window


def query_metric_window(metric_name: str, minutes: int = 60, dimensions: dict[str, str] | None = None, statistic: str = "Average"):
    start_time, end_time = infer_time_window(minutes)
    window = MetricWindow(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=dimensions or {}, statistic=statistic)
    client = ObservabilityClient()
    return client.query_series(metric_name=metric_name, start_time=window.start_time, end_time=window.end_time, dimensions=window.dimensions, statistic=window.statistic, period=window.period)
