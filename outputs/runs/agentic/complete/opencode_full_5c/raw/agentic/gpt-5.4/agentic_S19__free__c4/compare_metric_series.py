from __future__ import annotations

from statistics import mean
from typing import Dict, Optional

from observability_models import ComparisonResult, MetricWindowRequest
from query_metric_window import query_metric_window


def _average_for_filter(
    project_id: str,
    metric_type: str,
    start_time,
    end_time,
    dimensions: Dict[str, str],
) -> Optional[float]:
    response = query_metric_window(
        MetricWindowRequest(
            project_id=project_id,
            metric_type=metric_type,
            start_time=start_time,
            end_time=end_time,
            filter_labels=dimensions,
        )
    )
    values = [point.value for point in response.points if point.value is not None]
    return mean(values) if values else None


def compare_metric_series(
    project_id: str,
    metric_type: str,
    start_time,
    end_time,
    left_dimensions: Dict[str, str],
    right_dimensions: Dict[str, str],
) -> ComparisonResult:
    left_average = _average_for_filter(
        project_id, metric_type, start_time, end_time, left_dimensions
    )
    right_average = _average_for_filter(
        project_id, metric_type, start_time, end_time, right_dimensions
    )
    delta = (
        None
        if left_average is None or right_average is None
        else left_average - right_average
    )
    ratio = (
        None
        if right_average in (None, 0) or left_average is None
        else left_average / right_average
    )
    return ComparisonResult(
        metric_type=metric_type,
        left_label=str(left_dimensions),
        right_label=str(right_dimensions),
        left_average=left_average,
        right_average=right_average,
        delta=delta,
        ratio=ratio,
    )
