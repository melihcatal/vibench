from __future__ import annotations

from typing import Dict, Optional

from observability_client import GoogleCloudMonitoringClient, merge_dimension_filters
from observability_models import MetricPoint, MetricWindowRequest, SeriesComparisonResult, average_point_value, normalize_time_series_point


def _fetch_points(
    client: GoogleCloudMonitoringClient,
    request: MetricWindowRequest,
    resource_labels: Optional[Dict[str, str]] = None,
) -> list[MetricPoint]:
    scoped_request = MetricWindowRequest(
        project_id=request.project_id,
        metric_type=request.metric_type,
        start_time=request.start_time,
        end_time=request.end_time,
        alignment_period_seconds=request.alignment_period_seconds,
        per_series_aligner=request.per_series_aligner,
        resource_type=request.resource_type,
        resource_labels=merge_dimension_filters(request.resource_labels, resource_labels),
    )
    payload = client.list_time_series(scoped_request, view="FULL")
    points: list[MetricPoint] = []
    for series in payload.get("timeSeries", []):
        for point in series.get("points", []):
            points.append(normalize_time_series_point(series, point))
    points.sort(key=lambda p: p.interval_end)
    return points


def compare_metric_series(
    request: MetricWindowRequest,
    left_resource_labels: Dict[str, str],
    right_resource_labels: Dict[str, str],
    left_label: str = "left",
    right_label: str = "right",
) -> SeriesComparisonResult:
    client = GoogleCloudMonitoringClient(project_id=request.project_id)
    left_points = _fetch_points(client, request, left_resource_labels)
    right_points = _fetch_points(client, request, right_resource_labels)
    left_avg = average_point_value(left_points)
    right_avg = average_point_value(right_points)
    return SeriesComparisonResult(
        metric_type=request.metric_type,
        left_label=left_label,
        right_label=right_label,
        left_points=left_points,
        right_points=right_points,
        left_average=left_avg,
        right_average=right_avg,
        average_delta=left_avg - right_avg,
    )
