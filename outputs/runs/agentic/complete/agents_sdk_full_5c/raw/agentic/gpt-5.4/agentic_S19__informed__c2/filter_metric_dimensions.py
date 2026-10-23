from __future__ import annotations

from typing import Dict, Optional

from observability_client import GoogleCloudObservabilityClient
from observability_models import MetricWindowRequest, MetricWindowResponse, normalize_time_series


def _build_dimension_filter(resource_labels: Optional[Dict[str, str]] = None, metric_labels: Optional[Dict[str, str]] = None) -> str:
    clauses = []
    for key, value in (resource_labels or {}).items():
        clauses.append(f'resource.labels.{key} = "{value}"')
    for key, value in (metric_labels or {}).items():
        clauses.append(f'metric.labels.{key} = "{value}"')
    return " AND ".join(clauses)


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
    minutes: int = 30,
    interval_seconds: int = 60,
) -> MetricWindowResponse:
    client = GoogleCloudObservabilityClient()
    request = MetricWindowRequest(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        interval_seconds=interval_seconds,
        filter_expression=_build_dimension_filter(resource_labels, metric_labels),
        aggregation_aligner="mean",
    )
    series = client.list_time_series(request)
    points = normalize_time_series(series)
    return MetricWindowResponse(metric_type=metric_type, points=points)
