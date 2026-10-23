from __future__ import annotations

from datetime import datetime
from statistics import mean

from observability_client import get_google_cloud_project_id, list_time_series
from observability_models import (
    AggregatedMetricStats,
    MetricWindowRequest,
    flatten_values,
    isoformat_z,
    series_to_model,
)


def aggregate_metric_stats(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    project_id: str | None = None,
    alignment_period_seconds: int = 300,
    per_series_aligner: str = "ALIGN_MEAN",
    resource_type: str | None = None,
    filter_clauses: list[str] | None = None,
) -> AggregatedMetricStats:
    request = MetricWindowRequest(
        project_id=get_google_cloud_project_id(project_id),
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
        resource_type=resource_type,
        filter_clauses=filter_clauses or [],
    )
    series = [series_to_model(item) for item in list_time_series(request)]
    values = flatten_values(series)
    return AggregatedMetricStats(
        metric_type=metric_type,
        start_time=isoformat_z(start_time),
        end_time=isoformat_z(end_time),
        point_count=len(values),
        min_value=min(values) if values else None,
        max_value=max(values) if values else None,
        mean_value=mean(values) if values else None,
        sum_value=sum(values) if values else None,
    )
