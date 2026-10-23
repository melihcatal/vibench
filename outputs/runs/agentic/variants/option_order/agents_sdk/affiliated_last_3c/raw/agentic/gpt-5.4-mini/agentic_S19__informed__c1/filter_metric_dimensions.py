from __future__ import annotations

from observability_client import client


def filter_metric_dimensions(metric_name: str, dimensions: dict[str, str], minutes: int = 60):
    return client().filter_by_dimensions(metric_name, dimensions=dimensions, minutes=minutes)
