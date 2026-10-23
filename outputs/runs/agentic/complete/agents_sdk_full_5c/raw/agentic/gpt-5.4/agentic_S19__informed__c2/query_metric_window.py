from __future__ import annotations

from observability_client import GoogleCloudObservabilityClient
from observability_models import MetricWindowRequest, MetricWindowResponse, normalize_time_series


def query_metric_window(
    project_id: str,
    metric_type: str,
    minutes: int = 15,
    interval_seconds: int = 60,
) -> MetricWindowResponse:
    client = GoogleCloudObservabilityClient()
    request = MetricWindowRequest(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        interval_seconds=interval_seconds,
        aggregation_aligner="mean",
    )
    series = client.list_time_series(request)
    points = normalize_time_series(series)
    return MetricWindowResponse(metric_type=metric_type, points=points)
