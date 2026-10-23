from __future__ import annotations

from observability_client import fetch_metric_series
from observability_models import (
    MetricComparisonResponse,
    MetricWindowRequest,
    isoformat_utc,
    normalize_dimensions,
)


def compare_metric_series(
    metric_name: str,
    start_time,
    end_time,
    namespace: str,
    left_dimensions: dict[str, str],
    right_dimensions: dict[str, str],
    period: int = 60,
    stat: str = "Average",
    left_label: str = "left",
    right_label: str = "right",
) -> MetricComparisonResponse:
    left_request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=normalize_dimensions(left_dimensions),
    )
    right_request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=normalize_dimensions(right_dimensions),
    )
    left_points = fetch_metric_series(left_request)
    right_points = fetch_metric_series(right_request)
    left_average = (
        sum(point.value for point in left_points) / len(left_points)
        if left_points
        else None
    )
    right_average = (
        sum(point.value for point in right_points) / len(right_points)
        if right_points
        else None
    )
    delta_average = None
    if left_average is not None and right_average is not None:
        delta_average = left_average - right_average
    return MetricComparisonResponse(
        metric_name=metric_name,
        namespace=namespace,
        left_label=left_label,
        right_label=right_label,
        start_time=isoformat_utc(left_request.start_time),
        end_time=isoformat_utc(left_request.end_time),
        stat=stat,
        left_points=left_points,
        right_points=right_points,
        left_average=left_average,
        right_average=right_average,
        delta_average=delta_average,
    )
