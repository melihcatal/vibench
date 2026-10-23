from __future__ import annotations

from typing import Optional

from observability_client import monitoring_client
from observability_models import MetricWindowRequest, MetricWindowResponse, normalize_time_series_points


def query_metric_window(
    metric_type: str,
    minutes: int = 60,
    project_id: Optional[str] = None,
    alignment_period_seconds: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
    filter_text: Optional[str] = None,
) -> MetricWindowResponse:
    client = monitoring_client(project_id)
    request = MetricWindowRequest(
        project_id=client.project_id,
        metric_type=metric_type,
        minutes=minutes,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
        filter_text=filter_text,
    )
    payload = client.list_time_series(request=request, view="FULL")
    points = normalize_time_series_points(payload.get("timeSeries", []))
    return MetricWindowResponse(metric_type=metric_type, points=points)
