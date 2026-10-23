from __future__ import annotations

from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricStatsResult, MetricWindowRequest, average_point_value, normalize_time_series_point, to_rfc3339


def aggregate_metric_stats(request: MetricWindowRequest, statistic: str = "mean") -> MetricStatsResult:
    client = GoogleCloudMonitoringClient(project_id=request.project_id)
    payload = client.list_time_series(request, view="FULL")

    points = []
    for series in payload.get("timeSeries", []):
        for point in series.get("points", []):
            points.append(normalize_time_series_point(series, point))

    values = [point.value for point in points]
    if not values:
        aggregated_value = 0.0
    elif statistic == "max":
        aggregated_value = max(values)
    elif statistic == "min":
        aggregated_value = min(values)
    elif statistic == "sum":
        aggregated_value = sum(values)
    else:
        aggregated_value = average_point_value(points)
        statistic = "mean"

    return MetricStatsResult(
        metric_type=request.metric_type,
        statistic=statistic,
        value=aggregated_value,
        start_time=to_rfc3339(request.start_time),
        end_time=to_rfc3339(request.end_time),
    )
