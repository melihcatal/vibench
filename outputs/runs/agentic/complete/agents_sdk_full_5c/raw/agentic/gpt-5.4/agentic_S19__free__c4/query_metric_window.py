from __future__ import annotations

from typing import List

from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricSeriesResult, MetricWindowRequest, normalize_time_series_point


def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResult:
    client = GoogleCloudMonitoringClient(project_id=request.project_id)
    payload = client.list_time_series(request, view="FULL")

    points: List = []
    series = payload.get("timeSeries", [])
    for item in series:
        for point in item.get("points", []):
            points.append(normalize_time_series_point(item, point))

    points.sort(key=lambda p: p.interval_end)
    return MetricSeriesResult(
        metric_type=request.metric_type,
        points=points,
        series_count=len(series),
    )
