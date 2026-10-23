from __future__ import annotations

from observability_client import CloudWatchMetricsClient
from observability_models import MetricWindowRequest, MetricSeriesPoint, normalize_datetime


def query_metric_window(request: MetricWindowRequest) -> list[MetricSeriesPoint]:
    client = CloudWatchMetricsClient()
    response = client.list_metric_data(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        dimensions=request.dimensions,
        period=request.period,
        stat=request.statistic,
    )
    timestamps = response.get("Datapoints", [])
    points: list[MetricSeriesPoint] = []
    for item in timestamps:
        value = item.get(request.statistic, item.get("Average"))
        if value is None:
            continue
        points.append(
            MetricSeriesPoint(
                timestamp=normalize_datetime(item["Timestamp"]),
                value=float(value),
                unit=item.get("Unit"),
                dimensions=request.dimensions,
            )
        )
    return sorted(points, key=lambda p: p.timestamp)
