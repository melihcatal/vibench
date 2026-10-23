"""
Queries recent datapoints for a named metric over a time window.

Provider: Datadog Metrics API (datadog-api-client)
Uses datadog_api_client.v1.api.metrics_api.MetricsApi and the api.datadoghq.com endpoint.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Tuple

from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi

from observability_client import ObservabilityClient
from observability_models import (
    MetricDataPoint,
    MetricQueryRequest,
    MetricTimeWindow,
    normalize_datadog_response,
)


def query_metric_window(
    metric_name: str,
    window: Optional[MetricTimeWindow] = None,
    aggregation: str = "avg",
    tags: Optional[dict] = None,
    rollup_interval: Optional[int] = None,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> List[MetricDataPoint]:
    """
    Query recent datapoints for a named metric over a time window using Datadog.

    Calls Datadog GET /api/v1/query endpoint via datadog_api_client SDK.

    Args:
        metric_name: Datadog metric name, e.g. 'system.cpu.usage'
        window: Time window for the query; defaults to last 60 minutes.
        aggregation: Aggregation function (avg, sum, min, max, count, last).
        tags: Dict of tag key-value pairs to filter by.
        rollup_interval: Optional rollup interval in seconds.
        api_key: Datadog API key (or set DATADOG_API_KEY env var).
        app_key: Datadog App key (or set DATADOG_APP_KEY env var).

    Returns:
        List of MetricDataPoint objects with timestamps and values.
    """
    if window is None:
        window = MetricTimeWindow.from_now(minutes_ago=60)

    query_request = MetricQueryRequest(
        metric_name=metric_name,
        time_window=window,
        aggregation=aggregation,  # type: ignore[arg-type]
        tags=tags or {},
        rollup_interval=rollup_interval,
    )

    client = ObservabilityClient(api_key=api_key, app_key=app_key)
    try:
        metrics_api: MetricsApi = client.get_v1_api()

        # Build Datadog query string
        query_string = query_request.to_datadog_query_string()
        start_ts, end_ts = window.to_datadog_timestamps()

        # Call Datadog Metrics API v1 GET /api/v1/query
        raw_response = metrics_api.query_metrics(
            _from=start_ts,
            to=end_ts,
            query=query_string,
        )

        # Normalize response
        data_points = normalize_datadog_response(raw_response)
        return data_points
    finally:
        client.close()


def query_metric_with_pagination(
    metric_name: str,
    minutes_ago: int = 60,
    tags: Optional[dict] = None,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> Tuple[List[MetricDataPoint], str]:
    """
    Query metric data with pagination support via Datadog API.

    Returns data points and the query expression used.
    """
    window = MetricTimeWindow.from_now(minutes_ago=minutes_ago)
    data_points = query_metric_window(
        metric_name=metric_name,
        window=window,
        tags=tags,
        api_key=api_key,
        app_key=app_key,
    )
    query_expr = f"avg:{metric_name}"
    if tags:
        tag_parts = [f"{k}:{v}" for k, v in tags.items()]
        query_expr += "{" + ",".join(tag_parts) + "}"
    return data_points, query_expr
