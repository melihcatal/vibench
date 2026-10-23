"""
aggregate_metric_stats.py
Retrieves aggregated statistics for a metric over a time window using the Datadog API.
Provider: Datadog (api.datadoghq.com)
"""

import os
import math
from typing import List, Optional, Dict, Any

from observability_client import get_metrics_api_v1, get_metrics_api_v2, load_datadog_config
from observability_models import (
    MetricStats,
    MetricSeries,
    compute_stats_from_series,
    normalize_datadog_series_to_metric_series,
    build_datadog_query_body,
)


def aggregate_metric_stats(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    aggregation: str = "avg",
    tags: Optional[List[str]] = None,
    group_by: Optional[List[str]] = None,
) -> List[MetricStats]:
    """
    Retrieve aggregated statistics for a Datadog metric over a time window.

    Uses the Datadog Metrics API v1 query endpoint to fetch raw series data,
    then computes local aggregate statistics (min, max, avg, std_dev, percentiles).

    Args:
        metric_name: The Datadog metric name, e.g. "system.cpu.user".
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.
        aggregation: Datadog aggregation (avg, sum, max, min, count).
        tags: Optional tag filters like ["env:production"].
        group_by: Optional group-by dimensions like ["host", "region"].

    Returns:
        List of MetricStats objects with computed aggregate statistics.
    """
    configuration = load_datadog_config()
    api = get_metrics_api_v1(configuration)
    api_client = api.api_client

    query_string = f"{aggregation}:{metric_name}"
    if tags:
        query_string += "{" + ",".join(tags) + "}"

    try:
        raw_response = api_client.call_api(
            resource_path="/api/v1/query",
            method="GET",
            query_params={
                "from": int(start_ts),
                "to": int(end_ts),
                "query": query_string,
            },
            response_type=dict,
        )

        if isinstance(raw_response, tuple):
            raw_response = raw_response[0]

        stats_results = []
        for raw_series in raw_response.get("series", []):
            metric_series = normalize_datadog_series_to_metric_series(
                raw_series=raw_series,
                metric_name=metric_name,
                start_time=start_ts,
                end_time=end_ts,
            )
            stats = compute_stats_from_series(metric_series)
            stats_results.append(stats)

        return stats_results

    except Exception as exc:
        raise RuntimeError(
            f"Datadog aggregate_metric_stats failed for metric '{metric_name}': {exc}"
        ) from exc


def aggregate_metric_with_percentiles(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    percentiles: List[float] = None,
    tags: Optional[List[str]] = None,
) -> MetricStats:
    """
    Get metric statistics including specific percentile values from Datadog.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        percentiles: List of percentiles to compute (default [50, 95, 99]).
        tags: Optional tag filters.

    Returns:
        MetricStats with computed percentiles.
    """
    if percentiles is None:
        percentiles = [50.0, 95.0, 99.0]

    stats_list = aggregate_metric_stats(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        tags=tags,
    )

    if not stats_list:
        return MetricStats(
            metric_name=metric_name,
            start_time=start_ts,
            end_time=end_ts,
            aggregation="avg",
            count=0, avg=None, min=None, max=None, sum=None,
            std_dev=None, p50=None, p95=None, p99=None,
        )

    # If there are multiple grouped series, merge them for aggregate stats
    if len(stats_list) == 1:
        return stats_list[0]

    merged_values = []
    for stats in stats_list:
        raw_series_data = aggregate_metric_stats(
            metric_name=metric_name,
            start_ts=start_ts,
            end_ts=end_ts,
            tags=tags,
        )
        for s in raw_series_data:
            if s.avg is not None:
                merged_values.append(s.avg)

    if not merged_values:
        return stats_list[0]

    count = len(merged_values)
    avg_val = sum(merged_values) / count
    min_val = min(merged_values)
    max_val = max(merged_values)
    sum_val = sum(merged_values)
    variance = sum((v - avg_val) ** 2 for v in merged_values) / max(count - 1, 1)
    std_val = variance ** 0.5
    sorted_vals = sorted(merged_values)

    def percentile(data, p):
        idx = int(len(data) * p / 100.0)
        return data[min(idx, len(data) - 1)]

    return MetricStats(
        metric_name=metric_name,
        start_time=start_ts,
        end_time=end_ts,
        aggregation=aggregation,
        count=count,
        avg=round(avg_val, 4),
        min=min_val,
        max=max_val,
        sum=round(sum_val, 4),
        std_dev=round(std_val, 4),
        p50=percentile(sorted_vals, 50),
        p95=percentile(sorted_vals, 95),
        p99=percentile(sorted_vals, 99),
    )


def aggregate_metric_rate(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    interval_seconds: int = 60,
    tags: Optional[List[str]] = None,
) -> List[MetricStats]:
    """
    Compute per-interval aggregate statistics for a metric from Datadog.

    Splits the time window into intervals and computes stats for each.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        interval_seconds: Duration of each aggregation interval.
        tags: Optional tag filters.

    Returns:
        List of MetricStats, one per interval.
    """
    results = []
    current_start = start_ts
    while current_start < end_ts:
        current_end = min(current_start + interval_seconds, end_ts)
        stats = aggregate_metric_stats(
            metric_name=metric_name,
            start_ts=current_start,
            end_ts=current_end,
            tags=tags,
        )
        if stats:
            for s in stats:
                results.append(s)
        current_start = current_end

    return results
