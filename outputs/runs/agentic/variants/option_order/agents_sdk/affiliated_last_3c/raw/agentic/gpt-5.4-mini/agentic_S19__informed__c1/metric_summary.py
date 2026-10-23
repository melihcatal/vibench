from __future__ import annotations

from observability_client import client
from observability_models import MetricWindow


def metric_summary(metric_name: str, minutes: int = 60, **kwargs):
    return client().summarize(MetricWindow.recent(metric_name, minutes=minutes, **kwargs))
