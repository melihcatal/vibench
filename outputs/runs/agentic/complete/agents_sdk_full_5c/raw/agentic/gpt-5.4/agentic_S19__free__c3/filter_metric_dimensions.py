from __future__ import annotations

from typing import Dict, Optional

from observability_client import monitoring_client
from observability_models import MetricWindowRequest, MetricWindowResponse, normalize_time_series_points


def _dimension_filter(resource_labels: Optional[Dict[str, str]], metric_labels: Optional[Dict[str, str]]) -> str:
    parts = []
    for key, value in (resource_labels or {}).items():
        parts.append(f'resource.labels.{key} = "{value}"')
    for key, value in (metric_labels or {}).items():
        parts.append(f'metric.labels.{key} = "{value}"')
    return " AND ".join(parts)


def filter_metric_dimensions(
    metric_type: str,
    minutes: int = 60,
    project_id: Optional[str] = None,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
) -> MetricWindowResponse:
    client = monitoring_client(project_id)
    request = MetricWindowRequest(
        project_id=client.project_id,
        metric_type=metric_type,
        minutes=minutes,
        alignment_period_seconds=60,
        per_series_aligner="ALIGN_MEAN",
        filter_text=_dimension_filter(resource_labels, metric_labels) or None,
    )
    payload = client.list_time_series(request=request, view="FULL")
    points = normalize_time_series_points(payload.get("timeSeries", []))
    return MetricWindowResponse(metric_type=metric_type, points=points)
