from __future__ import annotations

from statistics import mean
from typing import Dict, Optional

from filter_metric_dimensions import filter_metric_dimensions
from observability_models import MetricComparisonResult


def compare_metric_series(
    metric_type: str,
    left_resource_labels: Optional[Dict[str, str]] = None,
    right_resource_labels: Optional[Dict[str, str]] = None,
    left_metric_labels: Optional[Dict[str, str]] = None,
    right_metric_labels: Optional[Dict[str, str]] = None,
    minutes: int = 60,
    project_id: Optional[str] = None,
    left_label: str = "left",
    right_label: str = "right",
) -> MetricComparisonResult:
    left = filter_metric_dimensions(
        metric_type=metric_type,
        minutes=minutes,
        project_id=project_id,
        resource_labels=left_resource_labels,
        metric_labels=left_metric_labels,
    )
    right = filter_metric_dimensions(
        metric_type=metric_type,
        minutes=minutes,
        project_id=project_id,
        resource_labels=right_resource_labels,
        metric_labels=right_metric_labels,
    )
    left_avg = mean(left.values()) if left.values() else None
    right_avg = mean(right.values()) if right.values() else None
    delta = None if left_avg is None or right_avg is None else left_avg - right_avg
    ratio = None if left_avg is None or right_avg in (None, 0) else left_avg / right_avg
    return MetricComparisonResult(
        left_label=left_label,
        right_label=right_label,
        left_average=left_avg,
        right_average=right_avg,
        delta=delta,
        ratio=ratio,
    )
