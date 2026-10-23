from __future__ import annotations

from observability_client import CloudWatchMetricsClient
from observability_models import MetricSeriesPoint, MetricWindowRequest, normalize_dimensions


def filter_metric_dimensions(request: MetricWindowRequest, allowed_dimensions: dict[str, str]) -> list[MetricSeriesPoint]:
    client = CloudWatchMetricsClient()
    dims = normalize_dimensions(allowed_dimensions)
    response = client.list_metric_data(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        dimensions=dims,
        period=request.period,
        stat=request.statistic,
    )
    points: list[MetricSeriesPoint] = []
    for item in response.get("Datapoints", []):
        value = item.get(request.statistic, item.get("Average"))
        if value is None:
            continue
        points.append(MetricSeriesPoint(timestamp=item["Timestamp"], value=float(value), unit=item.get("Unit"), dimensions=dims))
    return points
