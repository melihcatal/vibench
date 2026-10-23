from __future__ import annotations

from observability_client import build_list_request, build_monitoring_client
from observability_models import (
    MetricComparisonResponse,
    MetricWindowRequest,
    flatten_values,
    normalize_time_series,
    to_rfc3339,
)


def compare_metric_series(
    left: MetricWindowRequest, right: MetricWindowRequest
) -> MetricComparisonResponse:
    if left.metric_type != right.metric_type:
        raise ValueError("Both comparison requests must use the same metric_type")
    client = build_monitoring_client()
    left_series = normalize_time_series(
        list(client.list_time_series(request=build_list_request(left, view="FULL")))
    )
    right_series = normalize_time_series(
        list(client.list_time_series(request=build_list_request(right, view="FULL")))
    )
    left_values = flatten_values(left_series)
    right_values = flatten_values(right_series)
    left_average = (sum(left_values) / len(left_values)) if left_values else None
    right_average = (sum(right_values) / len(right_values)) if right_values else None
    delta = (
        None
        if left_average is None or right_average is None
        else left_average - right_average
    )
    ratio = (
        None
        if left_average is None or right_average in (None, 0)
        else left_average / right_average
    )
    return MetricComparisonResponse(
        metric_type=left.metric_type,
        start_time=to_rfc3339(left.start_time),
        end_time=to_rfc3339(left.end_time),
        left_average=left_average,
        right_average=right_average,
        delta=delta,
        ratio=ratio,
    )
