from __future__ import annotations

from typing import Dict, List, Optional

from observability_client import ObservabilityClient, create_client
from observability_models import (
    MetricDataPoint,
    MetricTimeSeries,
    normalize_datadog_series,
)


def filter_metric_dimensions(
    metric_name: str,
    start: int,
    end: int,
    dimension_filters: Optional[Dict[str, str]] = None,
    group_by: Optional[List[str]] = None,
    interval: Optional[int] = None,
    client: Optional[ObservabilityClient] = None,
) -> List[MetricTimeSeries]:
    tags = []
    if dimension_filters:
        for key, value in dimension_filters.items():
            tags.append(f"{key}:{value}")

    tag_filter_str = ""
    if tags:
        tag_filter_str = "{" + ",".join(tags) + "}"

    query_str = f"{metric_name}{tag_filter_str}"

    if client is None:
        client = create_client()

    params = {
        "from": start,
        "to": end,
        "query": query_str,
    }
    if interval is not None:
        params["interval"] = interval
    if group_by:
        params["group_by"] = ",".join(group_by)

    response = client.query_metrics_v1(
        query=query_str,
        start=start,
        end=end,
        interval=interval,
    )

    series_list = []
    for raw_series in response.get("series", []):
        series = normalize_datadog_series(raw_series, metric_name)
        series_list.append(series)

    return series_list


def filter_metric_dimensions_points(
    metric_name: str,
    start: int,
    end: int,
    dimension_filters: Optional[Dict[str, str]] = None,
    group_by: Optional[List[str]] = None,
    interval: Optional[int] = None,
    client: Optional[ObservabilityClient] = None,
) -> Dict[str, List[MetricDataPoint]]:
    series_list = filter_metric_dimensions(
        metric_name=metric_name,
        start=start,
        end=end,
        dimension_filters=dimension_filters,
        group_by=group_by,
        interval=interval,
        client=client,
    )

    grouped_points: Dict[str, List[MetricDataPoint]] = {}
    for series in series_list:
        tag_key = _build_tag_key(series.tag_set)
        grouped_points[tag_key] = sorted(series.points, key=lambda p: p.timestamp)

    return grouped_points


def _build_tag_key(tag_set: Optional[Dict[str, str]]) -> str:
    if not tag_set:
        return "ungrouped"
    parts = [f"{k}={v}" for k, v in sorted(tag_set.items())]
    return ",".join(parts)
