"""
Query recent datapoints for a named metric over a time window.
Uses the Datadog Metrics API (datadog_api_client) as the concrete provider.
Provider: Datadog (api.datadoghq.com)
"""

from typing import List, Optional

from observability_client import (
    get_metrics_api_client,
    build_time_window,
    build_metric_query_string,
    normalize_datadog_metric_response,
)
from observability_models import (
    MetricDataPoint,
    MetricSeries,
    MetricQueryResponse,
    parse_datadog_response_to_model,
)


def query_metric_window(
    metric_name: str,
    minutes_ago: Optional[int] = None,
    hours_ago: Optional[int] = None,
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
    aggregation: str = "avg",
    filter_tags: Optional[dict] = None,
) -> MetricQueryResponse:
    """
    Query recent datapoints for a named metric over a time window using Datadog API.

    Args:
        metric_name: The Datadog metric name (e.g. 'system.cpu.user').
        minutes_ago: How many minutes back to query.
        hours_ago: How many hours back to query.
        start_ts: Explicit start timestamp (epoch seconds).
        end_ts: Explicit end timestamp (epoch seconds).
        aggregation: Datadog aggregation function (avg, sum, max, min, etc.).
        filter_tags: Optional dict of tag key-value pairs for filtering.

    Returns:
        MetricQueryResponse containing the queried series and data points.
    """
    from_ts, to_ts = build_time_window(
        minutes_ago=minutes_ago,
        hours_ago=hours_ago,
        start_ts=start_ts,
        end_ts=end_ts,
    )

    query_string = build_metric_query_string(
        metric_name=metric_name,
        aggregation=aggregation,
        filter_tags=filter_tags,
    )

    metrics_api = get_metrics_api_client()

    raw_response = metrics_api.query_metrics(
        _from=from_ts,
        to=to_ts,
        query=query_string,
    )

    normalized = parse_datadog_response_to_model(raw_response)
    return normalized


def get_raw_metric_points(
    metric_name: str,
    minutes_ago: int = 60,
    aggregation: str = "avg",
    filter_tags: Optional[dict] = None,
) -> List[MetricDataPoint]:
    """
    Convenience function to retrieve a flat list of data points for a metric.

    Args:
        metric_name: The Datadog metric name.
        minutes_ago: How many minutes back to query.
        aggregation: Aggregation function.
        filter_tags: Optional tag filters.

    Returns:
        Flat list of MetricDataPoint objects across all series.
    """
    response = query_metric_window(
        metric_name=metric_name,
        minutes_ago=minutes_ago,
        aggregation=aggregation,
        filter_tags=filter_tags,
    )

    all_points: List[MetricDataPoint] = []
    for series in response.series:
        all_points.extend(series.points)
    return all_points
