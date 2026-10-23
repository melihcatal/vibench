"""
compare_metric_series.py - Compares metric values for two resources or dimension filters
over the same time window. Uses Datadog Metrics API (api.datadoghq.com).
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
    build_tagged_request,
)
from observability_models import (
    MetricQueryResponse,
    MetricSeries,
    MetricStats,
    compute_series_stats,
)


def compare_metric_series(
    metric_name: str,
    series_a_tags: List[str],
    series_b_tags: List[str],
    window_minutes: int = 60,
    to_ts: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Compare metric values for two sets of dimension filters over the same window.

    Issues two parallel Datadog queries (one per tag set) and computes
    comparative statistics.

    Args:
        metric_name: The Datadog metric identifier.
        series_a_tags: Tag filters for the first series (e.g. ["env:production"]).
        series_b_tags: Tag filters for the second series (e.g. ["env:staging"]).
        window_minutes: Number of minutes to look back.
        to_ts: Optional end timestamp (epoch seconds). Defaults to now.

    Returns:
        Dict with comparison results for both series.
    """
    config = DatadogConfig()
    client = DatadogMetricsClient(config)

    request_a = build_tagged_request(
        metric_name=metric_name,
        tags=series_a_tags,
        window_minutes=window_minutes,
        to_ts=to_ts,
    )

    response_a = client.query(request_a)

    request_b = build_tagged_request(
        metric_name=metric_name,
        tags=series_b_tags,
        window_minutes=window_minutes,
        to_ts=to_ts,
    )

    response_b = client.query(request_b)

    return _build_comparison(response_a, response_b, series_a_tags, series_b_tags)


def _build_comparison(
    response_a: MetricQueryResponse,
    response_b: MetricQueryResponse,
    tags_a: List[str],
    tags_b: List[str],
) -> Dict[str, Any]:
    """Build the comparison result from two query responses."""
    stats_a = _aggregate_response(response_a)
    stats_b = _aggregate_response(response_b)

    comparison: Dict[str, Any] = {
        "series_a": {
            "tags": tags_a,
            "point_count": stats_a.get("count", 0),
            "avg": stats_a.get("avg", 0.0),
            "min": stats_a.get("min", 0.0),
            "max": stats_a.get("max", 0.0),
            "sum": stats_a.get("sum", 0.0),
            "stddev": stats_a.get("stddev"),
        },
        "series_b": {
            "tags": tags_b,
            "point_count": stats_b.get("count", 0),
            "avg": stats_b.get("avg", 0.0),
            "min": stats_b.get("min", 0.0),
            "max": stats_b.get("max", 0.0),
            "sum": stats_b.get("sum", 0.0),
            "stddev": stats_b.get("stddev"),
        },
    }

    # Compute delta
    if stats_a.get("count", 0) > 0 and stats_b.get("count", 0) > 0:
        avg_a = stats_a["avg"]
        avg_b = stats_b["avg"]
        delta = avg_b - avg_a
        pct_change = (delta / abs(avg_a) * 100) if avg_a != 0 else 0.0

        comparison["delta"] = {
            "avg_diff": round(delta, 6),
            "pct_change": round(pct_change, 2),
            "series_a_higher": avg_a > avg_b,
        }

    comparison["window_from"] = response_a.from_ts
    comparison["window_to"] = response_a.to_ts

    return comparison


def _aggregate_response(response: MetricQueryResponse) -> Dict[str, Any]:
    """Aggregate all series in a response into combined stats."""
    all_values: List[float] = []
    for series in response.series:
        all_values.extend(series.values())

    if not all_values:
        return {"count": 0, "avg": 0.0, "min": 0.0, "max": 0.0, "sum": 0.0}

    combined_series = MetricSeries(
        metric_name=response.query,
        display_name=response.query,
        points=[
            type('Point', (), {'timestamp': 0, 'value': v})()  # type: ignore
            for v in all_values
        ],
    )

    # Rebuild with proper MetricPoint
    from observability_models import MetricPoint
    combined_series.points = [MetricPoint(timestamp=0, value=v) for v in all_values]

    stats = compute_series_stats(combined_series)

    return {
        "count": stats.count,
        "avg": stats.avg,
        "min": stats.min,
        "max": stats.max,
        "sum": stats.sum,
        "stddev": stats.stddev,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compare two Datadog metric series by dimension tags."
    )
    parser.add_argument("metric_name", help="Datadog metric name")
    parser.add_argument(
        "--series-a",
        nargs="+",
        required=True,
        help="Tag filters for series A (e.g. env:production)",
    )
    parser.add_argument(
        "--series-b",
        nargs="+",
        required=True,
        help="Tag filters for series B (e.g. env:staging)",
    )
    parser.add_argument(
        "--window", type=int, default=60, help="Time window in minutes"
    )

    args = parser.parse_args()

    result = compare_metric_series(
        metric_name=args.metric_name,
        series_a_tags=args.series_a,
        series_b_tags=args.series_b,
        window_minutes=args.window,
    )

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
