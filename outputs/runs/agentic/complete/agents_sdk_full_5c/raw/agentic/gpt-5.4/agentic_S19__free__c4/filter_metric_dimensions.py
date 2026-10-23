from __future__ import annotations

from typing import Dict, List, Optional

from observability_client import GoogleCloudMonitoringClient, merge_dimension_filters
from observability_models import MetricSeriesResult, MetricWindowRequest, normalize_time_series_point


def filter_metric_dimensions(
    request: MetricWindowRequest,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
) -> MetricSeriesResult:
    client = GoogleCloudMonitoringClient(project_id=request.project_id)
    merged_resource_labels = merge_dimension_filters(request.resource_labels, resource_labels)
    filter_expression = client.build_filter(
        metric_type=request.metric_type,
        resource_type=request.resource_type,
        resource_labels=merged_resource_labels,
        metric_labels=metric_labels,
    )

    params_request = MetricWindowRequest(
        project_id=request.project_id,
        metric_type=request.metric_type,
        start_time=request.start_time,
        end_time=request.end_time,
        alignment_period_seconds=request.alignment_period_seconds,
        per_series_aligner=request.per_series_aligner,
        resource_type=request.resource_type,
        resource_labels=merged_resource_labels,
    )
    payload = client.list_time_series(params_request, view="FULL")

    filtered_points: List = []
    for series in payload.get("timeSeries", []):
        for point in series.get("points", []):
            normalized = normalize_time_series_point(series, point)
            metric_match = all(normalized.metric_labels.get(k) == v for k, v in (metric_labels or {}).items())
            if metric_match:
                filtered_points.append(normalized)

    filtered_points.sort(key=lambda p: p.interval_end)
    return MetricSeriesResult(
        metric_type=f"{request.metric_type}|{filter_expression}",
        points=filtered_points,
        series_count=len(payload.get("timeSeries", [])),
    )
