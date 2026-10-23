from __future__ import annotations

from observability_client import ObservabilityClient
from observability_models import infer_time_window


def aggregate_metric_stats(metric_name: str, minutes: int = 60, dimensions: dict[str, str] | None = None):
    start_time, end_time = infer_time_window(minutes)
    client = ObservabilityClient()
    return client.get_statistics(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=dimensions)
