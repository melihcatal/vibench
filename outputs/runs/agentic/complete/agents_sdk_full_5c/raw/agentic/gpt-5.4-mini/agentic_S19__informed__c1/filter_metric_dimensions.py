from __future__ import annotations

from datetime import timedelta

from observability_client import DatadogMetricsClient, utc_now
from observability_models import MetricSeriesResponse, MetricWindowRequest, serialize_datapoints


def filter_metric_dimensions(metric_name: str, dimensions: dict[str, str], minutes: int = 30) -> MetricSeriesResponse:
    end_time = utc_now()
    request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=end_time - timedelta(minutes=minutes),
        end_time=end_time,
        dimensions=dimensions,
    )
    client = DatadogMetricsClient()
    payload = client.query_series(request)
    series = payload.get("series", [{}])[0]
    points = series.get("pointlist", [])
    datapoints = serialize_datapoints(
        {"timestamp": point[0] / 1000.0 if isinstance(point, list) and point else None, "value": point[1], "dimensions": dimensions}
        for point in points if point
    )
    return MetricSeriesResponse(metric_name=metric_name, datapoints=datapoints, raw=payload)
