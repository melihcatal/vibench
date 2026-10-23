from __future__ import annotations

from typing import List, Optional

from observability_client import ObservabilityClient, create_client
from observability_models import (
    MetricDataPoint,
    MetricQueryRequest,
    MetricTimeSeries,
    normalize_datadog_series,
)


def query_metric_window(
    metric_name: str,
    start: int,
    end: int,
    interval: Optional[int] = None,
    tags: Optional[List[str]] = None,
    client: Optional[ObservabilityClient] = None,
) -> List[MetricTimeSeries]:
    request = MetricQueryRequest(
        metric_name=metric_name,
        start=start,
        end=end,
        interval=interval,
        tags=tags,
    )

    if client is None:
        client = create_client()

    query_str = request.to_datadog_query()
    params = request.to_datadog_params()

    response = client.query_metrics_v1(
        query=query_str,
        start=params["from"],
        end=params["to"],
        interval=params.get("interval"),
    )

    series_list = []
    for raw_series in response.get("series", []):
        series = normalize_datadog_series(raw_series, metric_name)
        series_list.append(series)

    return series_list


def query_metric_window_points(
    metric_name: str,
    start: int,
    end: int,
    interval: Optional[int] = None,
    tags: Optional[List[str]] = None,
    client: Optional[ObservabilityClient] = None,
) -> List[MetricDataPoint]:
    series_list = query_metric_window(
        metric_name=metric_name,
        start=start,
        end=end,
        interval=interval,
        tags=tags,
        client=client,
    )

    all_points = []
    for series in series_list:
        all_points.extend(series.points)

    all_points.sort(key=lambda p: p.timestamp)
    return all_points
