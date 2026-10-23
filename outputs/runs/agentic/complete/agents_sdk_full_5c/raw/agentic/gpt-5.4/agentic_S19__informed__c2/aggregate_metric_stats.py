from __future__ import annotations

from observability_client import GoogleCloudObservabilityClient
from observability_models import MetricStatistics, MetricWindowRequest, compute_basic_stats, normalize_time_series


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    minutes: int = 60,
    interval_seconds: int = 300,
    aligner: str = "mean",
) -> MetricStatistics:
    client = GoogleCloudObservabilityClient()
    request = MetricWindowRequest(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        interval_seconds=interval_seconds,
        aggregation_aligner=aligner,
    )
    series = client.list_time_series(request)
    points = normalize_time_series(series)
    return compute_basic_stats(points, metric_type)
