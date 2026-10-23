"""
Retrieve aggregated statistics for a metric over a time window.
Uses the Datadog Metrics Query API (datadog_api_client) as the concrete provider.
Provider: Datadog (api.datadoghq.com)
"""

from typing import Optional, Dict, Any, List

from datadog_api_client.v1.api.metrics_api import MetricsApi

from observability_client import (
    get_metrics_api_client,
    build_time_window,
    build_metric_query_string,
)
from observability_models import (
    MetricAggregationStats,
    MetricQueryResponse,
    MetricDataPoint,
    parse_datadog_response_to_model,
    compute_percentile,
)


def aggregate_metric_stats(
    metric_name: str,
    minutes_ago: Optional[int] = None,
    hours_ago: Optional[int] = None,
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
    aggregation: str = "avg",
    filter_tags: Optional[Dict[str, str]] = None,
) -> List[MetricAggregationStats]:
    """
    Retrieve aggregated statistics for a metric over a time window using Datadog.

    Fetches the raw metric series and computes count, sum, avg, min, max,
    and percentile statistics (p50, p90, p99) from the returned data points.

    Args:
        metric_name: The Datadog metric name (e.g. 'system.cpu.user').
        minutes_ago: How many minutes back to aggregate.
        hours_ago: How many hours back to aggregate.
        start_ts: Explicit start timestamp (epoch seconds).
        end_ts: Explicit end timestamp (epoch seconds).
        aggregation: Datadog aggregation function.
        filter_tags: Optional dict of tag key-value pairs.

    Returns:
        List of MetricAggregationStats, one per metric series returned.
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

    parsed = parse_datadog_response_to_model(raw_response)

    results: List[MetricAggregationStats] = []
    for series in parsed.series:
        values = series.values()
        if not values:
            continue

        stats = MetricAggregationStats(
            metric_name=series.metric,
            count=len(values),
            sum_value=sum(values),
            avg_value=sum(values) / len(values),
            min_value=min(values),
            max_value=max(values),
            p50_value=compute_percentile(values, 50),
            p90_value=compute_percentile(values, 90),
            p99_value=compute_percentile(values, 99),
            start_ts=from_ts,
            end_ts=to_ts,
        )
        results.append(stats)

    return results


def get_aggregated_stats_as_dict(
    metric_name: str,
    minutes_ago: int = 60,
    aggregation: str = "avg",
    filter_tags: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Convenience function returning aggregated stats as a list of dicts.

    Args:
        metric_name: The Datadog metric name.
        minutes_ago: Window in minutes.
        aggregation: Aggregation type.
        filter_tags: Optional tag filters.

    Returns:
        List of dicts with aggregation statistics.
    """
    stats_list = aggregate_metric_stats(
        metric_name=metric_name,
        minutes_ago=minutes_ago,
        aggregation=aggregation,
        filter_tags=filter_tags,
    )
    return [s.to_dict() for s in stats_list]
