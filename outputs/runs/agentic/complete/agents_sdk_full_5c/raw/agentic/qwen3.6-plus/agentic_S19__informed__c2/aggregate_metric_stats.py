"""
Retrieve aggregated statistics for a metric over a time window using Datadog Metrics API.

Uses the Datadag Metrics API to compute aggregated statistics (avg, min, max, sum, count)
for a specified metric over a given time window. Provider: Datadog (DD_API_KEY, DD_APP_KEY).
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
    MetricAggregation,
    MetricSeries,
    parse_datadog_query_response,
    compute_aggregation,
)

DATADOG_QUERY_ENDPOINT = "https://api.datadoghq.com/api/v1/query"


def aggregate_metric_stats(
    metric_name: str,
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    window_minutes: int = 60,
    aggregator: str = "avg",
) -> list[MetricAggregation]:
    """
    Retrieve aggregated statistics for a metric over a time window from Datadog.

    Args:
        metric_name: Datadog metric name.
        from_ts: Optional start epoch seconds.
        to_ts: Optional end epoch seconds.
        window_minutes: Window duration in minutes.
        aggregator: Primary aggregation function for the query.

    Returns:
        List of MetricAggregation objects with computed stats.
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

    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    series_list = parse_datadog_query_response(data)

    aggregations = []
    for series in series_list:
        agg = compute_aggregation(series)
        aggregations.append(agg)

    return aggregations


def aggregate_metric_stats_with_percentiles(
    metric_name: str,
    tag_filters: Optional[list[str]] = None,
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    window_minutes: int = 60,
) -> MetricAggregation:
    """
    Retrieve aggregated statistics including percentiles from Datadog.

    Fetches metric data and computes additional percentile statistics locally.

    Args:
        metric_name: Datadog metric name.
        tag_filters: Optional tag filters for the query.
        from_ts: Optional start epoch seconds.
        to_ts: Optional end epoch seconds.
        window_minutes: Window duration in minutes.

    Returns:
        MetricAggregation with computed percentiles.
    """
    normalized = normalize_metric_name(metric_name)
    start, end = build_time_window(window_minutes)
    if from_ts is not None:
        start = from_ts
    if to_ts is not None:
        end = to_ts

    tag_clause = ""
    if tag_filters:
        tag_clause = ",".join(tag_filters)
    query_str = f"{normalized}{{{tag_clause}}}"

    session = create_datadog_session()
    url = build_datadog_query_url()

    params = {
        "query": query_str,
        "from": start,
        "to": end,
        "aggregator": "avg",
    }

    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    series_list = parse_datadog_query_response(data)

    all_values = []
    merged_tags: dict[str, str] = {}
    for series in series_list:
        all_values.extend(series.values)
        merged_tags.update(series.tag_set)

    if not all_values:
        return MetricAggregation(
            metric=metric_name,
            avg=0.0, min_val=0.0, max_val=0.0,
            sum_val=0.0, count=0, tag_set=merged_tags,
        )

    sorted_vals = sorted(all_values)
    n = len(sorted_vals)
    percentiles = {
        "p50": sorted_vals[int(n * 0.50)],
        "p90": sorted_vals[int(n * 0.90)],
        "p95": sorted_vals[int(n * 0.95)],
        "p99": sorted_vals[min(int(n * 0.99), n - 1)],
    }

    agg = MetricAggregation(
        metric=metric_name,
        avg=sum(all_values) / len(all_values),
        min_val=min(all_values),
        max_val=max(all_values),
        sum_val=sum(all_values),
        count=len(all_values),
        percentiles=percentiles,
        tag_set=merged_tags,
    )
    return agg
