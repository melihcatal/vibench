"""
filter_metric_dimensions.py - Queries metric data filtered by resource labels or dimensions.
Uses Datadog Metrics API (api.datadoghq.com) to retrieve metric data scoped by tags/dimensions.
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
from observability_models import MetricPoint, MetricQueryResponse, MetricSeries


def filter_metric_dimensions(
    metric_name: str,
    dimension_filters: Dict[str, str],
    window_minutes: int = 60,
    to_ts: Optional[int] = None,
) -> MetricQueryResponse:
    """
    Query metric data filtered by resource labels/dimensions.

    Converts dimension key-value pairs into Datadog tag filters
    (e.g. {"env": "production", "region": "us-east-1"} becomes
    ["env:production", "region:us-east-1"]).

    Args:
        metric_name: The Datadog metric identifier.
        dimension_filters: Dict of dimension name to value to filter on.
        window_minutes: Number of minutes to look back.
        to_ts: Optional end timestamp (epoch seconds). Defaults to now.

    Returns:
        MetricQueryResponse with filtered time series data.
    """
    tags = [f"{k}:{v}" for k, v in dimension_filters.items()]

    config = DatadogConfig()
    client = DatadogMetricsClient(config)

    request = build_tagged_request(
        metric_name=metric_name,
        tags=tags,
        window_minutes=window_minutes,
        to_ts=to_ts,
    )

    return client.query(request)


def get_unique_dimension_values(
    response: MetricQueryResponse,
) -> Dict[str, List[str]]:
    """
    Extract unique dimension/tag values from the returned series.

    Parses the scope field of each series to discover the actual
    dimension combinations that matched the query.
    """
    dimension_values: Dict[str, set] = {}

    for series in response.series:
        if series.scope:
            parts = series.scope.split(",")
            for part in parts:
                part = part.strip()
                if ":" in part:
                    key, value = part.split(":", 1)
                    if key not in dimension_values:
                        dimension_values[key] = set()
                    dimension_values[key].add(value)

    return {k: sorted(v) for k, v in dimension_values.items()}


def format_filtered_result(
    response: MetricQueryResponse,
    dimension_filters: Dict[str, str],
) -> Dict[str, Any]:
    """Format the filtered query result for output."""
    result: Dict[str, Any] = {
        "query": response.query,
        "dimension_filters": dimension_filters,
        "from_ts": response.from_ts,
        "to_ts": response.to_ts,
        "status": response.status,
        "series_count": len(response.series),
        "series": [],
    }

    for series in response.series:
        series_data: Dict[str, Any] = {
            "metric": series.metric_name,
            "display_name": series.display_name,
            "scope": series.scope,
            "unit": series.unit,
            "point_count": len(series.points),
            "points": [
                {"timestamp": p.timestamp, "value": p.value}
                for p in series.points
            ],
        }
        result["series"].append(series_data)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Query Datadog metric data filtered by resource dimensions/tags."
    )
    parser.add_argument("metric_name", help="Datadog metric name")
    parser.add_argument(
        "--window", type=int, default=60, help="Time window in minutes"
    )
    parser.add_argument(
        "--dimension",
        nargs=2,
        action="append",
        metavar=("KEY", "VALUE"),
        help="Dimension filter (repeatable, e.g. --dimension env production)",
    )

    args = parser.parse_args()

    if not args.dimension:
        parser.error("At least one --dimension KEY VALUE pair is required")

    dimension_filters = {k: v for k, v in args.dimension}

    response = filter_metric_dimensions(
        metric_name=args.metric_name,
        dimension_filters=dimension_filters,
        window_minutes=args.window,
    )

    result = format_filtered_result(response, dimension_filters)

    unique_dims = get_unique_dimension_values(response)
    if unique_dims:
        result["discovered_dimensions"] = unique_dims

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
