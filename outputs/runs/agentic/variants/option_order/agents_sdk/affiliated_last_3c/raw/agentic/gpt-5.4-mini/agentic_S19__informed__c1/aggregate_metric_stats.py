from __future__ import annotations

from observability_client import client
from observability_models import MetricWindow


def aggregate_metric_stats(metric_name: str, minutes: int = 60, statistic: str = "avg", **kwargs):
    window = MetricWindow.recent(metric_name, minutes=minutes, statistic=statistic, **kwargs)
    return client().aggregate(window)
