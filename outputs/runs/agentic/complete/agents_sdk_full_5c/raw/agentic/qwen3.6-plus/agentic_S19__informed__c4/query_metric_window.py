"""
Query recent datapoints for a named metric over a time window.

Uses the Datadog Metrics API (api.datadoghq.com) to fetch raw metric
datapoints for a given metric name within a start/end epoch-second window.
"""

import os
import requests
from typing import List, Optional, Dict, Any

from observability_client import (
    load_datadog_config,
    build_datadog_session,
    normalize_timestamps,
    format_datadog_query,
)
from observability_models import (
    MetricQueryRequest,
    MetricQueryResponse,
    parse_datadog_query_response,
    normalize_dimensions,
)


def query_metric_window(
    metric_name: str,
    start_ts: int,
    end_ts: int,
    aggregation: str = "avg",
    rollup: int = 60,
    dimensions: Optional[Dict[str, str]] = None,
    group_by: Optional[List[str]] = None,
    config: Optional[Dict[str, str]] = None,
) -> MetricQueryResponse:
    """Query recent datapoints for a named metric over a time window.

    Calls the Datadog Metrics API GET /api/v1/query endpoint to retrieve
    raw datapoints for the specified metric within [start_ts, end_ts].

    Args:
        metric_name: The Datadog metric name, e.g., 'system.cpu.usage'.
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.
        aggregation: Aggregation function (avg, sum, min, max).
        rollup: Rollup interval in seconds (default 60).
        dimensions: Optional tag filters, e.g., {'host': 'web-1'}.
        group_by: Optional list of tag keys to group results by.
        config: Optional Datadog config dict; loaded from env if omitted.

    Returns:
        MetricQueryResponse with parsed series and datapoints.
    """
    # Validate timestamps
    start_ts, end_ts = normalize_timestamps(start_ts, end_ts)

    # Normalize dimensions
    norm_dims = normalize_dimensions(dimensions)

    # Build the Datadog query string
    query_str = format_datadog_query(
        metric_name=metric_name,
        rollup=aggregation,
        aggregation=aggregation,
        dimensions=norm_dims if norm_dims else None,
    )

    # Build authenticated session
    if config is None:
        config = load_datadog_config()
    session = build_datadog_session(config)

    # Construct query parameters for Datadog API v1 /api/v1/query
    params: Dict[str, Any] = {
        "query": query_str,
        "from": start_ts,
        "to": end_ts,
    }

    if group_by:
        params["group_by"] = group_by

    # Execute query against datadoghq.com
    api_url = f"{session.base_url}/api/v1/query"
    resp = session.get(api_url, params=params, timeout=30)
    resp.raise_for_status()

    raw_json = resp.json()
    return parse_datadog_query_response(raw_json)


def query_metric_window_raw(
    metric_name: str,
    start_ts: int,
    end_ts: int,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: str = "datadoghq.com",
    aggregation: str = "avg",
    dimensions: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Query metric datapoints and return raw JSON response.

    A convenience wrapper that accepts credentials directly.

    Args:
        metric_name: The metric to query.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        api_key: Datadog DD_API_KEY (defaults to env).
        app_key: Datadog DD_APP_KEY (defaults to env).
        site: Datadog site hostname (e.g., datadoghq.com, datadoghq.eu).
        aggregation: Aggregation function.
        dimensions: Optional tag filters.

    Returns:
        Raw JSON dict from Datadog API.
    """
    cfg = {
        "api_key": api_key or os.environ.get("DD_API_KEY", ""),
        "app_key": app_key or os.environ.get("DD_APP_KEY", ""),
        "site": site,
    }
    result = query_metric_window(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        aggregation=aggregation,
        dimensions=dimensions,
        config=cfg,
    )
    # Return the datapoints in a simple dict
    all_points = []
    for series in result.series:
        for dp in series.datapoints:
            all_points.append({
                "timestamp": dp.timestamp,
                "value": dp.value,
                "metric": dp.metric,
                "tags": dp.tags,
            })
    return {
        "query": result.query,
        "from_ts": result.from_ts,
        "to_ts": result.to_ts,
        "total_datapoints": result.total_datapoints,
        "series_count": len(result.series),
        "datapoints": all_points,
    }
