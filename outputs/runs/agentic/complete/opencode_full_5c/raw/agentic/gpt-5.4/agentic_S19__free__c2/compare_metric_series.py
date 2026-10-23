from __future__ import annotations

from datetime import datetime
from statistics import mean

from observability_client import get_google_cloud_project_id, list_time_series
from observability_models import (
    MetricComparisonResult,
    MetricWindowRequest,
    flatten_values,
    isoformat_z,
    series_to_model,
)


def compare_metric_series(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    left_filter_clauses: list[str],
    right_filter_clauses: list[str],
    project_id: str | None = None,
    resource_type: str | None = None,
    alignment_period_seconds: int = 60,
    per_series_aligner: str = "ALIGN_MEAN",
) -> MetricComparisonResult:
    resolved_project_id = get_google_cloud_project_id(project_id)
    left_request = MetricWindowRequest(
        project_id=resolved_project_id,
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
        resource_type=resource_type,
        filter_clauses=left_filter_clauses,
    )
    right_request = MetricWindowRequest(
        project_id=resolved_project_id,
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
        resource_type=resource_type,
        filter_clauses=right_filter_clauses,
    )
    left_values = flatten_values(
        [series_to_model(item) for item in list_time_series(left_request)]
    )
    right_values = flatten_values(
        [series_to_model(item) for item in list_time_series(right_request)]
    )
    left_mean = mean(left_values) if left_values else None
    right_mean = mean(right_values) if right_values else None
    absolute_delta = (
        None if left_mean is None or right_mean is None else left_mean - right_mean
    )
    percent_delta = None
    if absolute_delta is not None and right_mean not in (None, 0):
        percent_delta = (absolute_delta / right_mean) * 100.0
    return MetricComparisonResult(
        metric_type=metric_type,
        left_filter=" AND ".join(left_filter_clauses),
        right_filter=" AND ".join(right_filter_clauses),
        start_time=isoformat_z(start_time),
        end_time=isoformat_z(end_time),
        left_mean=left_mean,
        right_mean=right_mean,
        absolute_delta=absolute_delta,
        percent_delta=percent_delta,
    )
