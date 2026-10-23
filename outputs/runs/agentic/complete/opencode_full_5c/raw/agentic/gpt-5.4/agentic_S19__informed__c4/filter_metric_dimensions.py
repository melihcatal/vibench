from __future__ import annotations

from typing import Dict

from observability_models import (
    MetricSeriesResponse,
    MetricWindowRequest,
    normalize_dimensions,
)
from query_metric_window import query_metric_window


def filter_metric_dimensions(
    metric: str,
    start_time,
    end_time,
    dimensions: Dict[str, str],
    namespace: str = "AWS/EC2",
    period: int = 60,
    stat: str = "Average",
    region_name: str | None = None,
) -> MetricSeriesResponse:
    request = MetricWindowRequest(
        metric=metric,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat=stat,
        dimensions=normalize_dimensions(dimensions),
    )
    return query_metric_window(request, region_name=region_name)
