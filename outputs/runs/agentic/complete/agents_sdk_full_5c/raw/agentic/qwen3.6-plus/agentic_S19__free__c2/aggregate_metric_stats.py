"""
Retrieves aggregated statistics for a metric over a time window.

Provider: Datadog Metrics API v1 (datadog-api-client)
Uses datadog_api_client.v1.api.metrics_api.MetricsApi and the api.datadoghq.com endpoint.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi

from observability_client import ObservabilityClient
from observability_models import (
    MetricAggregateStats,
    MetricAggregation,
    MetricTimeWindow,
    normalize_aggregate_response,
)


def aggregate_metric_stats(
    metric_name: str,
    window: Optional[MetricTimeWindow] = None,
    aggregations: Optional[List[MetricAggregation]] = None,
    tags: Optional[Dict[str, str]] = None,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> MetricAggregateStats:
    """
    Retrieve aggregated statistics for a metric over a time window using Datadog.

    Calls Datadog GET /api/v1/query endpoint and computes aggregate stats
    from the returned series data via datadog_api_client SDK.

    Args:
        metric_name: Datadog metric name, e.g. 'system.memory.used'
        window: Time window; defaults to last 60 minutes.
        aggregations: List of aggregation types to compute.
        tags: Dict of tag key-value pairs for filtering.
        api_key: Datadog API key (or set DATADOG_API_KEY env var).
        app_key: Datadog App key (or set DATADOG_APP_KEY env var).

    Returns:
        MetricAggregateStats with min, max, avg, sum, count, and percentiles.
    """
    if window is None:
        window = MetricTimeWindow.from_now(minutes_ago=60)

    if aggregations is None:
        aggregations = [MetricAggregation.AVG]

    client = ObservabilityClient(api_key=api_key, app_key=app_key)
    try:
        metrics_api: MetricsApi = client.get_v1_api()

        all_points = []
        primary_agg = aggregations[0]

        # Query using the primary aggregation
        tag_parts = []
        if tags:
            tag_parts = [f"{k}:{v}" for k, v in tags.items()]

        query_string = f"{primary_agg.value}:{metric_name}"
        if tag_parts:
            query_string += "{" + ",".join(tag_parts) + "}"

        start_ts = int(window.start.timestamp())
        end_ts = int(window.end.timestamp())

        # Call Datadog Metrics API
        raw_response = metrics_api.query_metrics(
            _from=start_ts,
            to=end_ts,
            query=query_string,
        )

        # Also query for count and percentiles if needed
        stats = normalize_aggregate_response(
            raw_response,
            metric_name=metric_name,
            aggregation=primary_agg,
            window=window,
        )

        # If additional aggregations requested, enrich the stats
        if MetricAggregation.COUNT in aggregations and stats.count is None:
            count_query = f"count:{metric_name}"
            if tag_parts:
                count_query += "{" + ",".join(tag_parts) + "}"
            count_response = metrics_api.query_metrics(
                _from=start_ts,
                to=end_ts,
                query=count_query,
            )
            count_series = count_response.get("series", [])
            if count_series:
                total = sum(float(p[1]) for p in count_series[0].get("pointlist", []) if p[1] is not None)
                stats.count = int(total) if total else len(count_series[0].get("pointlist", []))

        # If min/max not available from avg query, fetch them
        if stats.min_value is None or stats.max_value is None:
            for agg in [MetricAggregation.MIN, MetricAggregation.MAX]:
                if agg in aggregations:
                    minmax_query = f"{agg.value}:{metric_name}"
                    if tag_parts:
                        minmax_query += "{" + ",".join(tag_parts) + "}"
                    minmax_response = metrics_api.query_metrics(
                        _from=start_ts,
                        to=end_ts,
                        query=minmax_query,
                    )
                    minmax_series = minmax_response.get("series", [])
                    if minmax_series:
                        values = [float(p[1]) for p in minmax_series[0].get("pointlist", []) if p[1] is not None]
                        if values:
                            if agg == MetricAggregation.MIN and (stats.min_value is None):
                                stats.min_value = min(values)
                            if agg == MetricAggregation.MAX and (stats.max_value is None):
                                stats.max_value = max(values)

        return stats
    finally:
        client.close()


def get_metric_distribution(
    metric_name: str,
    minutes_ago: int = 60,
    tags: Optional[Dict[str, str]] = None,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> Dict[str, float]:
    """
    Get a quick distribution summary of a metric over a time window.

    Returns dict with p50, p95, p99, min, max, avg values.
    """
    window = MetricTimeWindow.from_now(minutes_ago=minutes_ago)
    stats = aggregate_metric_stats(
        metric_name=metric_name,
        window=window,
        tags=tags,
        api_key=api_key,
        app_key=app_key,
    )
    return {
        "p50": stats.p50 or 0.0,
        "p95": stats.p95 or 0.0,
        "p99": stats.p99 or 0.0,
        "min": stats.min_value or 0.0,
        "max": stats.max_value or 0.0,
        "avg": stats.avg_value or 0.0,
    }
