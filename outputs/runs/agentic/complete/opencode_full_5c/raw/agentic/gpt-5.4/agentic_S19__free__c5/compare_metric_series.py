from __future__ import annotations

from typing import Dict, Optional

from observability_models import MetricComparison, MetricDimensionsRequest, build_filter
from query_metric_window import query_metric_window


def _average_for_filter(
    request: MetricDimensionsRequest,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
) -> tuple[str, Optional[float]]:
    filter_expression = build_filter(
        metric_type=request.metric_type,
        resource_type=request.resource_type,
        metric_labels=metric_labels or request.metric_labels,
        resource_labels=resource_labels or request.resource_labels,
        extra_filter=request.filter_expression,
    )
    scoped_request = MetricDimensionsRequest(
        metric_type=request.metric_type,
        start_time=request.start_time,
        end_time=request.end_time,
        project_id=request.project_id,
        alignment_period_seconds=request.alignment_period_seconds,
        per_series_aligner=request.per_series_aligner,
        filter_expression=filter_expression,
        view=request.view,
        resource_type=request.resource_type,
        metric_labels=metric_labels or request.metric_labels,
        resource_labels=resource_labels or request.resource_labels,
    )
    series = query_metric_window(scoped_request)
    values = [point.value for entry in series for point in entry.points]
    if not values:
        return filter_expression, None
    return filter_expression, sum(values) / len(values)


def compare_metric_series(
    base_request: MetricDimensionsRequest,
    left_resource_labels: Optional[Dict[str, str]] = None,
    right_resource_labels: Optional[Dict[str, str]] = None,
    left_metric_labels: Optional[Dict[str, str]] = None,
    right_metric_labels: Optional[Dict[str, str]] = None,
) -> MetricComparison:
    left_filter, left_average = _average_for_filter(
        base_request, left_resource_labels, left_metric_labels
    )
    right_filter, right_average = _average_for_filter(
        base_request, right_resource_labels, right_metric_labels
    )
    absolute_difference = None
    percent_difference = None
    if left_average is not None and right_average is not None:
        absolute_difference = left_average - right_average
        if right_average != 0:
            percent_difference = (absolute_difference / right_average) * 100.0
    return MetricComparison(
        metric_type=base_request.metric_type,
        left_filter=left_filter,
        right_filter=right_filter,
        left_average=left_average,
        right_average=right_average,
        absolute_difference=absolute_difference,
        percent_difference=percent_difference,
    )
