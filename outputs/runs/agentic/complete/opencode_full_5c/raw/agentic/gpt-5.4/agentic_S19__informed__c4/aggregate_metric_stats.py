from __future__ import annotations

from observability_models import (
    MetricStatsResponse,
    MetricWindowRequest,
    aggregate_points,
)
from query_metric_window import query_metric_window


def aggregate_metric_stats(
    request: MetricWindowRequest, region_name: str | None = None
) -> MetricStatsResponse:
    series = query_metric_window(request, region_name=region_name)
    return aggregate_points(
        metric=series.metric,
        namespace=series.namespace,
        start_time=request.start_iso(),
        end_time=request.end_iso(),
        points=series.points,
    )
