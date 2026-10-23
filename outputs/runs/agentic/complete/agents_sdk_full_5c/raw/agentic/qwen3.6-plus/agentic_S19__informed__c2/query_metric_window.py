"""
Query recent datapoints for a named metric over a time window using Datadog Metrics API.

Uses the Datadog v1 Query API to retrieve raw metric time series data
for a specified metric name and time window. Provider: Datadog (DD_API_KEY, DD_APP_KEY).
"""

from datetime import datetime, timezone
from typing import Optional

from observability_client import (
    create_datadog_session,
    build_datadog_query_url,
    build_time_window,
    normalize_metric_name,
)
from observability_models import (
    MetricQueryRequest,
    MetricSeries,
    MetricDataPoint,
    parse_datadog_query_response,
)

DATADOG_QUERY_ENDPOINT = "https://api.datadoghq.com/api/v1/query"


def query_metric_window(
    metric_name: str,
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    window_minutes: int = 60,
    aggregator: str = "avg",
    rollup: Optional[int] = None,
) -> list[MetricSeries]:
    """
    Query recent datapoints for a named metric over a time window from Datadog.

    Args:
        metric_name: Datadog metric name (e.g., "system.cpu.user").
        from_ts: Optional start epoch seconds.
        to_ts: Optional end epoch seconds.
        window_minutes: Window duration in minutes when timestamps not provided.
        aggregator: Datadog aggregation function (avg, sum, max, min).
        rollup: Optional rollup interval in seconds.

    Returns:
        List of MetricSeries objects containing datapoints.
    """
    normalized = normalize_metric_name(metric_name)
    start, end = build_time_window(window_minutes)
    if from_ts is not None:
        start = from_ts
    if to_ts is not None:
        end = to_ts

    query_str = f"{normalized}{{{}}}"

    session = create_datadog_session()
    url = build_datadog_query_url()

    params = {
        "query": query_str,
        "from": start,
        "to": end,
        "aggregator": aggregator,
    }
    if rollup is not None:
        params["rollup"] = rollup

    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    series_list = parse_datadog_query_response(data)
    return series_list


def query_metric_window_with_tags(
    metric_name: str,
    tag_filters: list[str],
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    window_minutes: int = 60,
    aggregator: str = "avg",
) -> list[MetricSeries]:
    """
    Query metric datapoints filtered by Datadog tag filters.

    Args:
        metric_name: Datadog metric name.
        tag_filters: List of tag filter strings (e.g., ["env:production", "host:web-01"]).
        from_ts: Optional start epoch seconds.
        to_ts: Optional end epoch seconds.
        window_minutes: Window duration in minutes.
        aggregator: Aggregation function.

    Returns:
        List of MetricSeries objects.
    """
    normalized = normalize_metric_name(metric_name)
    start, end = build_time_window(window_minutes)
    if from_ts is not None:
        start = from_ts
    if to_ts is not None:
        end = to_ts

    tag_clause = ",".join(tag_filters)
    query_str = f"{normalized}{{{tag_clause}}}"

    session = create_datadog_session()
    url = build_datadog_query_url()

    params = {
        "query": query_str,
        "from": start,
        "to": end,
        "aggregator": aggregator,
    }

    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    return parse_datadog_query_response(data)
