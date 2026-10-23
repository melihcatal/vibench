from __future__ import annotations

from typing import Any, Dict, Optional

from filter_metric_dimensions import filter_metric_dimensions
from observability_models import ComparisonResult, MetricPoint, compute_aggregate_stats


def compare_metric_series(
    project_id: str,
    metric_type: str,
    left_resource_labels: Optional[Dict[str, str]] = None,
    right_resource_labels: Optional[Dict[str, str]] = None,
    minutes: int = 15,
) -> Dict[str, Any]:
    left = filter_metric_dimensions(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        resource_labels=left_resource_labels or {},
    )
    right = filter_metric_dimensions(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        resource_labels=right_resource_labels or {},
    )
    left_stats = compute_aggregate_stats(metric_type, [MetricPoint(**point) for point in left["matched_points"]])
    right_stats = compute_aggregate_stats(metric_type, [MetricPoint(**point) for point in right["matched_points"]])
    delta = None
    ratio = None
    if left_stats.average is not None and right_stats.average is not None:
        delta = left_stats.average - right_stats.average
        ratio = (left_stats.average / right_stats.average) if right_stats.average not in (0, 0.0) else None
    result = ComparisonResult(
        left_label=str(left_resource_labels or {}),
        right_label=str(right_resource_labels or {}),
        left_average=left_stats.average,
        right_average=right_stats.average,
        delta=delta,
        ratio=ratio,
    )
    return result.__dict__
