from __future__ import annotations

from typing import Mapping, Optional

from aggregate_metric_stats import aggregate_metric_stats
from observability_models import MetricComparisonResponse


def compare_metric_series(
    metric_name: str,
    left_dimensions: Optional[Mapping[str, str]] = None,
    right_dimensions: Optional[Mapping[str, str]] = None,
    minutes: int = 60,
) -> MetricComparisonResponse:
    left = aggregate_metric_stats(metric_name=metric_name, minutes=minutes, dimensions=left_dimensions or {})
    right = aggregate_metric_stats(metric_name=metric_name, minutes=minutes, dimensions=right_dimensions or {})
    delta = float(left.statistics.get("average", 0.0) - right.statistics.get("average", 0.0))
    return MetricComparisonResponse(metric_name=metric_name, left=left, right=right, delta=delta)
