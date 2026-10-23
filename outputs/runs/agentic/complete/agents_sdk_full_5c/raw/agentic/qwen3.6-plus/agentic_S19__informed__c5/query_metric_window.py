"""
query_metric_window.py - Queries recent datapoints for a named metric over a time window.
Uses Datadog Metrics API (api.datadoghq.com) to retrieve time series data.
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
from observability_models import MetricPoint, MetricQueryResponse, MetricSeries


def query_metric_window(
    metric_name: str,
    window_minutes: int = 60,
    to_ts: Optional[int] = None,
    aggregation: Optional[str] = None,
    rollup: Optional[int] = None,
    tags: Optional[List[str]] = None,
) -> MetricQueryResponse:
    """
    Query recent datapoints for a named metric over a specified time window.

    Args:
        metric_name: The Datadog metric identifier (e.g. "system.cpu.idle").
        window_minutes: Number of minutes to look back.
        to_ts: Optional end timestamp (epoch seconds). Defaults to now.
        aggregation: Optional aggregation function (avg, sum, min, max, etc.).
        rollup: Optional rollup interval in seconds.
        tags: Optional list of tag filters (e.g. ["env:production", "region:us-east-1"]).

    Returns:
        MetricQueryResponse with normalized time series data.
    """
    config = DatadogConfig()
    client = DatadogMetricsClient(config)

    request = build_windowed_request(
        metric_name=metric_name,
        window_minutes=window_minutes,
        to_ts=to_ts,
        aggregation=aggregation,
        rollup=rollup,
        tags=tags,
    )

    return client.query(request)


def format_points(series: MetricSeries) -> List[Dict[str, Any]]:
    """Format metric points for JSON serialization."""
    return [
        {"timestamp": p.timestamp, "value": p.value}
        for p in series.points
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Query metric datapoints over a time window from Datadog."
    )
    parser.add_argument("metric_name", help="Datadog metric name")
    parser.add_argument(
        "--window", type=int, default=60, help="Time window in minutes"
    )
    parser.add_argument("--aggregation", default="avg", help="Aggregation function")
    parser.add_argument("--rollup", type=int, default=60, help="Rollup interval in seconds")
    parser.add_argument("--tags", nargs="*", help="Tag filters")

    args = parser.parse_args()

    response = query_metric_window(
        metric_name=args.metric_name,
        window_minutes=args.window,
        aggregation=args.aggregation,
        rollup=args.rollup,
        tags=args.tags,
    )

    result: Dict[str, Any] = {
        "query": response.query,
        "from_ts": response.from_ts,
        "to_ts": response.to_ts,
        "status": response.status,
        "series": [
            {
                "metric": s.metric_name,
                "display_name": s.display_name,
                "scope": s.scope,
                "unit": s.unit,
                "points": format_points(s),
            }
            for s in response.series
        ],
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
