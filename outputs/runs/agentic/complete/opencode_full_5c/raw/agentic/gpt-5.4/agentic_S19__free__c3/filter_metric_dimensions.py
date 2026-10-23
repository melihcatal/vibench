from __future__ import annotations

from observability_client import build_list_request, build_monitoring_client
from observability_models import (
    MetricWindowRequest,
    MetricWindowResponse,
    normalize_time_series,
)


def filter_metric_dimensions(
    metric_type: str,
    start_time,
    end_time,
    labels: dict[str, str],
    project_id: str | None = None,
    resource_type: str | None = None,
) -> MetricWindowResponse:
    request = MetricWindowRequest(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        project_id=project_id,
        resource_type=resource_type,
        labels=labels,
    )
    client = build_monitoring_client()
    pager = client.list_time_series(request=build_list_request(request, view="FULL"))
    return normalize_time_series(list(pager))
