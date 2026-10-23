from __future__ import annotations

from observability_client import build_list_request, build_monitoring_client
from observability_models import (
    MetricStatsResponse,
    MetricWindowRequest,
    flatten_values,
    normalize_time_series,
    to_rfc3339,
)


def aggregate_metric_stats(request: MetricWindowRequest) -> MetricStatsResponse:
    client = build_monitoring_client()
    pager = client.list_time_series(request=build_list_request(request, view="FULL"))
    normalized = normalize_time_series(list(pager))
    values = flatten_values(normalized)
    if not values:
        return MetricStatsResponse(
            metric_type=request.metric_type,
            start_time=to_rfc3339(request.start_time),
            end_time=to_rfc3339(request.end_time),
            sample_count=0,
            minimum=None,
            maximum=None,
            average=None,
            total=None,
        )
    total = sum(values)
    return MetricStatsResponse(
        metric_type=request.metric_type,
        start_time=to_rfc3339(request.start_time),
        end_time=to_rfc3339(request.end_time),
        sample_count=len(values),
        minimum=min(values),
        maximum=max(values),
        average=total / len(values),
        total=total,
    )
