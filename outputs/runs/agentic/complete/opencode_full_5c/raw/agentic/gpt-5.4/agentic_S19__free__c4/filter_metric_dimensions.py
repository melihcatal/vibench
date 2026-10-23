from __future__ import annotations

from observability_models import MetricSeriesResponse, MetricWindowRequest
from query_metric_window import query_metric_window


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    start_time,
    end_time,
    dimensions: dict[str, str],
    alignment_period_seconds: int = 300,
) -> MetricSeriesResponse:
    request = MetricWindowRequest(
        project_id=project_id,
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        filter_labels=dimensions,
        alignment_period_seconds=alignment_period_seconds,
    )
    return query_metric_window(request)
