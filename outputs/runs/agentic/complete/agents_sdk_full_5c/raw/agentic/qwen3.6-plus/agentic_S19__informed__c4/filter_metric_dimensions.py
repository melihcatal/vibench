"""
Query metric data filtered by resource labels or dimensions.

Uses the Datadog Metrics API (api.datadoghq.com) to fetch metric datapoints
filtered by specific tag/dimension values, enabling resource-level analysis.
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
    MetricSeries,
    parse_datadog_query_response,
    normalize_dimensions,
)


def filter_metric_dimensions(
    metric_name: str,
    start_ts: int,
    end_ts: int,
    dimensions: Dict[str, str],
    aggregation: str = "avg",
    config: Optional[Dict[str, str]] = None,
) -> MetricQueryResponse:
    """Query metric data filtered by resource labels or dimensions.

    Calls the Datadog Metrics API GET /api/v1/query endpoint with tag-based
    dimension filters to retrieve only datapoints matching the specified
    resource labels (e.g., host, region, environment).

    Args:
        metric_name: The Datadog metric name, e.g., 'system.cpu.usage'.
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.
        dimensions: Required tag filters, e.g., {'host': 'web-1', 'region': 'us-east-1'}.
        aggregation: Aggregation function (avg, sum, min, max).
        config: Optional Datadog config dict; loaded from env if omitted.

    Returns:
        MetricQueryResponse containing only filtered series.

    Raises:
        ValueError: If dimensions dict is empty.
    """
    if not dimensions:
        raise ValueError("dimensions must be provided to filter metric data")

    start_ts, end_ts = normalize_timestamps(start_ts, end_ts)
    norm_dims = normalize_dimensions(dimensions)

    if config is None:
        config = load_datadog_config()
    session = build_datadog_session(config)

    query_str = format_datadog_query(
        metric_name=metric_name,
        rollup=aggregation,
        aggregation=aggregation,
        dimensions=norm_dims,
    )

    params = {
        "query": query_str,
        "from": start_ts,
        "to": end_ts,
    }

    api_url = f"{session.base_url}/api/v1/query"
    resp = session.get(api_url, params=params, timeout=30)
    resp.raise_for_status()

    raw_json = resp.json()
    return parse_datadog_query_response(raw_json)


def filter_metric_dimensions_multi(
    metric_name: str,
    start_ts: int,
    end_ts: int,
    dimension_filters: List[Dict[str, str]],
    aggregation: str = "avg",
    config: Optional[Dict[str, str]] = None,
) -> Dict[str, MetricQueryResponse]:
    """Query metric data with multiple dimension filter sets.

    Executes parallel Datadog API queries for each set of dimensions,
    returning results keyed by a filter identifier string.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.
        dimension_filters: List of dimension dicts to query separately.
        aggregation: Aggregation function.
        config: Optional Datadog config dict.

    Returns:
        Dict mapping filter-description string to MetricQueryResponse.
    """
    if config is None:
        config = load_datadog_config()

    results: Dict[str, MetricQueryResponse] = {}

    for dim_set in dimension_filters:
        filter_key = ",".join(f"{k}={v}" for k, v in sorted(dim_set.items()))
        try:
            result = filter_metric_dimensions(
                metric_name=metric_name,
                start_ts=start_ts,
                end_ts=end_ts,
                dimensions=dim_set,
                aggregation=aggregation,
                config=config,
            )
            results[filter_key] = result
        except requests.RequestException as e:
            results[filter_key] = MetricQueryResponse(
                message=f"Error querying filter {filter_key}: {str(e)}"
            )

    return results


def get_metric_dimensions_list(
    metric_name: str,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: str = "datadoghq.com",
    limit: int = 100,
) -> List[str]:
    """Get available dimensions/tags for a metric from Datadog.

    Uses the Datadog API to list tags associated with a metric.

    Args:
        metric_name: The metric to inspect.
        api_key: Datadog DD_API_KEY.
        app_key: Datadog DD_APP_KEY.
        site: Datadog site hostname.
        limit: Maximum tags to return.

    Returns:
        List of dimension/tag names available for the metric.
    """
    cfg = {
        "api_key": api_key or os.environ.get("DD_API_KEY", ""),
        "app_key": app_key or os.environ.get("DD_APP_KEY", ""),
        "site": site,
    }
    session = build_datadog_session(cfg)

    api_url = f"{session.base_url}/api/v1/tags/{metric_name}"
    resp = session.get(api_url, params={"limit": limit}, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    return data.get("tags", [])
