from __future__ import annotations

from query_metric_window import query_metric_window
from observability_models import MetricSeriesResponse, MetricWindowRequest


GOOGLE_CLOUD_MONITORING_API = "https://monitoring.googleapis.com"


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    minutes: int = 15,
    resource_type: str | None = None,
    resource_labels: dict[str, str] | None = None,
    metric_labels: dict[str, str] | None = None,
    alignment_period_seconds: int = 60,
) -> MetricSeriesResponse:
    request = MetricWindowRequest(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        alignment_period_seconds=alignment_period_seconds,
        resource_type=resource_type,
        resource_labels=resource_labels or {},
        metric_labels=metric_labels or {},
    )
    return query_metric_window(request)
