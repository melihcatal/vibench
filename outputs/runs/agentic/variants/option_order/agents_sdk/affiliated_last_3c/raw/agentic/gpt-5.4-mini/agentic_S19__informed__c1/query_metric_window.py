from __future__ import annotations

from observability_client import client
from observability_models import MetricWindow


def query_metric_window(metric_name: str, minutes: int = 60, **kwargs):
    return client().query_recent(MetricWindow.recent(metric_name, minutes=minutes, **kwargs))
