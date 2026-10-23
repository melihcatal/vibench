from __future__ import annotations

from observability_client import run_query
from observability_models import MetricWindowRequest, MetricWindowResponse


def query_metric_window(request: MetricWindowRequest) -> MetricWindowResponse:
    return MetricWindowResponse(series=run_query(request), next_page_token=None)
