from __future__ import annotations

from observability_client import fetch_metric_series
from observability_models import (
    AggregateMetricStatsResponse,
    MetricWindowRequest,
    isoformat_utc,
)


def aggregate_metric_stats(
    request: MetricWindowRequest,
) -> AggregateMetricStatsResponse:
    points = fetch_metric_series(request)
    values = [point.value for point in points]
    unit = points[0].unit if points else None
    sample_count = len(values)
    total = sum(values) if values else None
    average = (total / sample_count) if values else None
    return AggregateMetricStatsResponse(
        metric_name=request.metric_name,
        namespace=request.namespace,
        start_time=isoformat_utc(request.start_time),
        end_time=isoformat_utc(request.end_time),
        sample_count=sample_count,
        minimum=min(values) if values else None,
        maximum=max(values) if values else None,
        average=average,
        sum=total,
        unit=unit,
    )
