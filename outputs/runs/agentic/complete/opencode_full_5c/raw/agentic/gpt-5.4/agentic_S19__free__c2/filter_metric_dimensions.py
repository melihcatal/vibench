from __future__ import annotations

from datetime import datetime

from observability_client import get_google_cloud_project_id, list_time_series
from observability_models import (
    MetricWindowRequest,
    MetricWindowResponse,
    isoformat_z,
    series_to_model,
)


def filter_metric_dimensions(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    resource_labels: dict[str, str] | None = None,
    metric_labels: dict[str, str] | None = None,
    project_id: str | None = None,
    resource_type: str | None = None,
    alignment_period_seconds: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
) -> MetricWindowResponse:
    filter_clauses: list[str] = []
    for key, value in (resource_labels or {}).items():
        filter_clauses.append(f'resource.labels.{key} = "{value}"')
    for key, value in (metric_labels or {}).items():
        filter_clauses.append(f'metric.labels.{key} = "{value}"')
    request = MetricWindowRequest(
        project_id=get_google_cloud_project_id(project_id),
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
        resource_type=resource_type,
        filter_clauses=filter_clauses,
    )
    series = [series_to_model(item) for item in list_time_series(request)]
    return MetricWindowResponse(
        project_id=request.project_id,
        metric_type=metric_type,
        start_time=isoformat_z(start_time),
        end_time=isoformat_z(end_time),
        series=series,
    )
