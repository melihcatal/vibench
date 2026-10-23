"""
query_metric_window.py
Queries recent datapoints for a named metric over a time window using the Datadog API.
Provider: Datadog (api.datadoghq.com)
"""

import os
import time
from typing import List, Optional, Dict, Any

from observability_client import get_metrics_api_v1, load_datadog_config
from observability_models import (
    MetricQueryRequest,
    MetricSeries,
    Datapoint,
    normalize_datadog_series_to_metric_series,
)


def query_metric_window(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    aggregation: str = "avg",
    host: Optional[str] = None,
    tags: Optional[List[str]] = None,
    rollup_interval: Optional[int] = None,
) -> List[MetricSeries]:
    """
    Query recent datapoints for a named metric over a specified time window
    using the Datadog Metrics API v1.

    Args:
        metric_name: The Datadog metric name, e.g. "system.cpu.user".
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.
        aggregation: Datadog aggregation function (avg, sum, max, min, count).
        host: Optional host filter.
        tags: Optional list of tag filters like ["env:production", "region:us-east-1"].
        rollup_interval: Optional rollup interval in seconds.

    Returns:
        List of MetricSeries objects containing the queried datapoints.
    """
    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_ts,
        end_time=end_ts,
        aggregation=aggregation,
        rollup_interval=rollup_interval,
        host_filter=host,
        tag_filters=tags,
    )

    query_string = request.to_datadog_query()

    configuration = load_datadog_config()
    api = get_metrics_api_v1(configuration)

    response = api.list_active_metrics(
        _from=int(start_ts),
        to=int(end_ts),
    )

    # Use the query endpoint for actual time-series data via v1 query
    from datadog_api_client.v1.api.metrics_api import MetricsApi
    api_client = api.api_client

    # Build query parameters for the query endpoint
    query_params = {
        "from": int(start_ts),
        "to": int(end_ts),
        "query": query_string,
    }

    if rollup_interval:
        query_params["rollup_interval"] = rollup_interval

    try:
        raw_response = api_client.call_api(
            resource_path="/api/v1/query",
            method="GET",
            query_params=query_params,
            response_type=dict,
        )

        if isinstance(raw_response, tuple):
            raw_response = raw_response[0]

        series_results = []
        for raw_series in raw_response.get("series", []):
            metric_series = normalize_datadog_series_to_metric_series(
                raw_series=raw_series,
                metric_name=metric_name,
                start_time=start_ts,
                end_time=end_ts,
            )
            series_results.append(metric_series)

        return series_results

    except Exception as exc:
        raise RuntimeError(
            f"Datadog query_metric_window failed for metric '{metric_name}': {exc}"
        ) from exc


def query_latest_datapoints(
    metric_name: str,
    lookback_seconds: int = 3600,
    aggregation: str = "avg",
    tags: Optional[List[str]] = None,
) -> List[MetricSeries]:
    """
    Query the latest datapoints for a metric within a lookback window.

    Args:
        metric_name: The Datadog metric name.
        lookback_seconds: How far back to query in seconds (default 1 hour).
        aggregation: Aggregation function.
        tags: Optional tag filters.

    Returns:
        List of MetricSeries with recent datapoints.
    """
    now = time.time()
    start = now - lookback_seconds
    return query_metric_window(
        metric_name=metric_name,
        start_ts=start,
        end_ts=now,
        aggregation=aggregation,
        tags=tags,
    )


def query_metric_with_rollup(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    rollup_seconds: int = 300,
    aggregation: str = "avg",
) -> List[MetricSeries]:
    """
    Query metric data with a specific rollup interval from Datadog.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        rollup_seconds: Rollup interval in seconds (default 5 minutes).
        aggregation: Aggregation function.

    Returns:
        List of MetricSeries with rolled-up datapoints.
    """
    return query_metric_window(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        aggregation=aggregation,
        rollup_interval=rollup_seconds,
    )
