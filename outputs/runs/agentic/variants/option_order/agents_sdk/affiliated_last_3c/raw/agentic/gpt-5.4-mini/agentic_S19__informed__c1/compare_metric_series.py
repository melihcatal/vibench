from __future__ import annotations

from observability_client import client


def compare_metric_series(metric_name: str, left_dimensions: dict[str, str], right_dimensions: dict[str, str], minutes: int = 60):
    return client().compare_series(metric_name, left_dimensions, right_dimensions, minutes=minutes)
