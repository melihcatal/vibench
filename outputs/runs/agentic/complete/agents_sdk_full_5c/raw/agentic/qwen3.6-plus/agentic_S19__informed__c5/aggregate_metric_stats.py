"""
aggregate_metric_stats.py - Retrieves aggregated statistics for a metric over a time window.
Uses Datadog Metrics API (api.datadoghq.com) to retrieve and compute aggregate statistics.
Provider: Datadog Metrics API v1
Auth: DD_API_KEY, DD_APP_KEY
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from observability_client import (
    DatadogConfig,
    DatadogMetricsClient,
    build_windowed_request,
)
from observability_models import (
    MetricQueryResponse,
    MetricSeries,
    MetricStats,
    compute_series_stats,
)


def aggregate_metric_stats(
    metric_name: str,
    window_minutes: int = 60,
    to_ts: Optional[int] = None,
    tags: Optional[List[str]] = None,
) -> List[MetricStats]:
    """
    Retrieve aggregated statistics for a metric over a specified time window.

    Queries Datadog for raw datapoints and computes count, avg, sum, min, max,
    and stddev across all points in the window.

    Args:
        metric_name: The Datadog metric identifier.
        window_minutes: Number of minutes to look back.
        to_ts: Optional end timestamp (epoch seconds). Defaults to now.
        tags: Optional list of tag filters for scoping the query.

    Returns:
        List of MetricStats, one per series returned by the query.
    """
    config = DatadogConfig()
    client = DatadogMetricsClient(config)

    request = build_windowed_request(
        metric_name=metric_name,
        window_minutes=window_minutes,
        to_ts=to_ts,
        aggregation="avg",
        rollup=60,
        tags=tags,
    )

    response = client.query(request)

    stats_list: List[MetricStats] = []
    for series in response.series:
        stats = compute_series_stats(series)
        stats.window_from = response.from_ts
        stats.window_to = response.to_ts
        stats.unit = series.unit
        stats_list.append(stats)

    return stats_list


def stats_to_dict(stats: MetricStats) -> Dict[str, Any]:
    """Convert MetricStats to a serializable dictionary."""
    return {
        "metric_name": stats.metric_name,
        "count": stats.count,
        "avg": round(stats.avg, 6),
        "sum": round(stats.sum, 6),
        "min": round(stats.min, 6),
        "max": round(stats.max, 6),
        "stddev": round(stats.stddev, 6) if stats.stddev is not None else None,
        "window_from": stats.window_from,
        "window_to": stats.window_to,
        "unit": stats.unit,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compute aggregated statistics for a Datadog metric over a time window."
    )
    parser.add_argument("metric_name", help="Datadog metric name")
    parser.add_argument(
        "--window", type=int, default=60, help="Time window in minutes"
    )
    parser.add_argument("--tags", nargs="*", help="Tag filters")

    args = parser.parse_args()

    stats_list = aggregate_metric_stats(
        metric_name=args.metric_name,
        window_minutes=args.window,
        tags=args.tags,
    )

    result: Dict[str, Any] = {
        "metrics": [stats_to_dict(s) for s in stats_list],
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
