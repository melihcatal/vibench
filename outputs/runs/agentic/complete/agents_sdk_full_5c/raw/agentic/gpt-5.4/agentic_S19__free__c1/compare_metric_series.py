from __future__ import annotations

from observability_models import ComparisonResult, MetricWindowRequest, average
from query_metric_window import query_metric_window


GOOGLE_MONITORING_CLIENT_CLASS = "google.cloud.monitoring_v3.MetricServiceClient"


def compare_metric_series(
    left_request: MetricWindowRequest,
    right_request: MetricWindowRequest,
    left_label: str = "left",
    right_label: str = "right",
) -> ComparisonResult:
    left = query_metric_window(left_request)
    right = query_metric_window(right_request)
    left_average = average(point.value for point in left.points)
    right_average = average(point.value for point in right.points)
    return ComparisonResult(
        metric_type=left_request.metric_type,
        interval_start=left.interval_start,
        interval_end=left.interval_end,
        left_label=left_label,
        right_label=right_label,
        left_points=left.points,
        right_points=right.points,
        left_average=left_average,
        right_average=right_average,
        difference=left_average - right_average,
    )
