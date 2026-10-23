from __future__ import annotations

from observability_client import fetch_metric_series
from observability_models import (
    MetricSeriesResponse,
    MetricWindowRequest,
    isoformat_utc,
)


def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResponse:
    points = fetch_metric_series(request)
    return MetricSeriesResponse(
        metric_name=request.metric_name,
        namespace=request.namespace,
        stat=request.stat,
        start_time=isoformat_utc(request.start_time),
        end_time=isoformat_utc(request.end_time),
        period=request.period,
        points=points,
    )
