"""
Retrieve aggregated statistics for a metric over a time window.

Uses the Datadog Metrics API (api.datadoghq.com) to fetch metric datapoints
and compute aggregated statistics (min, max, avg, sum, percentiles).
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
    MetricQueryResponse,
    MetricAggregationStats,
    parse_datadog_query_response,
    compute_aggregation_stats,
    normalize_dimensions,
)


def aggregate_metric_stats(
    metric_name: str,
    start_ts: int,
    end_ts: int,
    aggregation: str = "avg",
    rollup: int = 60,
    dimensions: Optional[Dict[str, str]] = None,
    config: Optional[Dict[str, str]] = None,
) -> List[MetricAggregationStats]:
    """Retrieve aggregated statistics for a metric over a time window.

    Queries the Datadog Metrics API GET /api/v1/query endpoint to retrieve
    raw datapoints, then computes aggregated statistics per series including
    min, max, avg, sum, count, and percentiles.

    Args:
        metric_name: The Datadog metric name, e.g., 'system.cpu.usage'.
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.
        aggregation: Aggregation function (avg, sum, min, max).
        rollup: Rollup interval in seconds.
        dimensions: Optional tag filters for the query.
        config: Optional Datadog config dict; loaded from env if omitted.

    Returns:
        List of MetricAggregationStats, one per metric series returned.
    """
    start_ts, end_ts = normalize_timestamps(start_ts, end_ts)
    norm_dims = normalize_dimensions(dimensions)

    if config is None:
        config = load_datadog_config()
    session = build_datadog_session(config)

    query_str = format_datadog_query(
        metric_name=metric_name,
        rollup=aggregation,
        aggregation=aggregation,
        dimensions=norm_dims if norm_dims else None,
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
    query_response = parse_datadog_query_response(raw_json)

    stats_list: List[MetricAggregationStats] = []
    for series in query_response.series:
        if series.datapoints:
            stats = compute_aggregation_stats(series.datapoints)
            stats_list.append(stats)

    return stats_list


def aggregate_metric_stats_summary(
    metric_name: str,
    start_ts: int,
    end_ts: int,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: str = "datadoghq.com",
    dimensions: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Retrieve aggregated stats and return a JSON-serializable summary.

    Convenience wrapper that returns a simple dict suitable for API responses.

    Args:
        metric_name: The metric to aggregate.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        api_key: Datadog DD_API_KEY.
        app_key: Datadog DD_APP_KEY.
        site: Datadog site hostname.
        dimensions: Optional tag filters.

    Returns:
        Dict with metric_name, stats fields, and series count.
    """
    cfg = {
        "api_key": api_key or os.environ.get("DD_API_KEY", ""),
        "app_key": app_key or os.environ.get("DD_APP_KEY", ""),
        "site": site,
    }
    stats_list = aggregate_metric_stats(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        dimensions=dimensions,
        config=cfg,
    )

    if not stats_list:
        return {"metric_name": metric_name, "series_count": 0, "stats": []}

    # If single series, return directly
    if len(stats_list) == 1:
        s = stats_list[0]
        return {
            "metric_name": s.metric_name,
            "series_count": 1,
            "tags": s.tags,
            "stats": {
                "min": s.min,
                "max": s.max,
                "avg": s.avg,
                "sum": s.sum,
                "count": s.count,
                "p50": s.percentile_50,
                "p95": s.percentile_95,
                "p99": s.percentile_99,
            },
        }

    # Multiple series: return each with its tags
    results = []
    for s in stats_list:
        results.append({
            "tags": s.tags,
            "stats": {
                "min": s.min,
                "max": s.max,
                "avg": s.avg,
                "sum": s.sum,
                "count": s.count,
                "p50": s.percentile_50,
                "p95": s.percentile_95,
                "p99": s.percentile_99,
            },
        })

    return {
        "metric_name": stats_list[0].metric_name,
        "series_count": len(stats_list),
        "stats": results,
    }
