from __future__ import annotations

from statistics import mean

from observability_client import run_query
from observability_models import (
    CompareMetricSeriesRequest,
    ComparedMetricSeries,
    MetricWindowRequest,
    values_from_points,
)


def compare_metric_series(request: CompareMetricSeriesRequest) -> ComparedMetricSeries:
    left_request = MetricWindowRequest(
        **{**request.base_request.__dict__, "labels": request.left_labels}
    )
    right_request = MetricWindowRequest(
        **{**request.base_request.__dict__, "labels": request.right_labels}
    )
    left_points = run_query(left_request)
    right_points = run_query(right_request)
    left_values = values_from_points(left_points)
    right_values = values_from_points(right_points)
    left_average = mean(left_values) if left_values else None
    right_average = mean(right_values) if right_values else None
    average_delta = (
        None
        if left_average is None or right_average is None
        else left_average - right_average
    )
    return ComparedMetricSeries(
        left_label_filter=request.left_labels,
        right_label_filter=request.right_labels,
        left_points=left_points,
        right_points=right_points,
        left_average=left_average,
        right_average=right_average,
        average_delta=average_delta,
    )
