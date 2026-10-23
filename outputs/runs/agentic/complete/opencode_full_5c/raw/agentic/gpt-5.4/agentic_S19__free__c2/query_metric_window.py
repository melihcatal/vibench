from __future__ import annotations

from datetime import datetime

from observability_client import get_google_cloud_project_id, list_time_series
from observability_models import (
    MetricWindowRequest,
    MetricWindowResponse,
    isoformat_z,
    series_to_model,
)


def query_metric_window(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    project_id: str | None = None,
    alignment_period_seconds: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
    resource_type: str | None = None,
    filter_clauses: list[str] | None = None,
) -> MetricWindowResponse:
    resolved_project_id = get_google_cloud_project_id(project_id)
    request = MetricWindowRequest(
        project_id=resolved_project_id,
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
        resource_type=resource_type,
        filter_clauses=filter_clauses or [],
    )
    series = [series_to_model(item) for item in list_time_series(request)]
    return MetricWindowResponse(
        project_id=resolved_project_id,
        metric_type=metric_type,
        start_time=isoformat_z(start_time),
        end_time=isoformat_z(end_time),
        series=series,
    )
