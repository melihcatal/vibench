from __future__ import annotations

from typing import Dict, Optional

from filter_metric_dimensions import filter_metric_dimensions
from observability_models import MetricComparison


def _average(values):
    if not values:
        return None
    return sum(values) / len(values)


def compare_metric_series(
    project_id: str,
    metric_type: str,
    left_resource_labels: Optional[Dict[str, str]] = None,
    right_resource_labels: Optional[Dict[str, str]] = None,
    minutes: int = 30,
    interval_seconds: int = 60,
) -> MetricComparison:
    left = filter_metric_dimensions(project_id, metric_type, resource_labels=left_resource_labels, minutes=minutes, interval_seconds=interval_seconds)
    right = filter_metric_dimensions(project_id, metric_type, resource_labels=right_resource_labels, minutes=minutes, interval_seconds=interval_seconds)

    left_avg = _average([point.value for point in left.points])
    right_avg = _average([point.value for point in right.points])
    absolute_delta = None if left_avg is None or right_avg is None else left_avg - right_avg
    percent_delta = None
    if absolute_delta is not None and right_avg not in (None, 0):
        percent_delta = (absolute_delta / right_avg) * 100.0

    return MetricComparison(
        left_label=str(left_resource_labels or {}),
        right_label=str(right_resource_labels or {}),
        left_average=left_avg,
        right_average=right_avg,
        absolute_delta=absolute_delta,
        percent_delta=percent_delta,
    )
