from __future__ import annotations

from observability_client import fetch_metric_series
from observability_models import (
    MetricSeriesResponse,
    MetricWindowRequest,
    isoformat_utc,
    normalize_dimensions,
)


def filter_metric_dimensions(
    metric_name: str,
    start_time,
    end_time,
    namespace: str,
    dimensions: dict[str, str],
    period: int = 60,
    stat: str = "Average",
) -> MetricSeriesResponse:
    request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=normalize_dimensions(dimensions),
    )
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
