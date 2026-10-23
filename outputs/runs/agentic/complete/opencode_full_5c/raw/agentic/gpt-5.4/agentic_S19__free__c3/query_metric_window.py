from __future__ import annotations

from observability_client import build_list_request, build_monitoring_client
from observability_models import (
    MetricWindowRequest,
    MetricWindowResponse,
    normalize_time_series,
)


def query_metric_window(request: MetricWindowRequest) -> MetricWindowResponse:
    client = build_monitoring_client()
    pager = client.list_time_series(request=build_list_request(request, view="FULL"))
    return normalize_time_series(list(pager))
