"""
Queries metric data filtered by resource labels or dimensions.

Provider: Datadog Metrics API (datadog-api-client)
Uses datadog_api_client.v1.api.metrics_api.MetricsApi and the api.datadoghq.com endpoint.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi

from observability_client import ObservabilityClient
from observability_models import (
    DimensionFilter,
    MetricDataPoint,
    MetricSeries,
    MetricTimeWindow,
    normalize_datadog_response,
)


def build_datadog_tag_filter(filters: List[DimensionFilter]) -> Dict[str, str]:
    """
    Convert DimensionFilter list into Datadog tag key-value dict.

    Datadog uses the tag format 'key:value'. This builds a dict of
    tag_name: tag_value pairs for the primary value of each filter.
    """
    tag_dict: Dict[str, str] = {}
    for f in filters:
        if f.operator == "in" and f.dimension_values:
            # Use first value as representative filter
            tag_dict[f.dimension_key] = f.dimension_values[0]
        elif f.operator == "exists":
            tag_dict[f.dimension_key] = "*"
    return tag_dict


def filter_metric_dimensions(
    metric_name: str,
    dimension_filters: List[DimensionFilter],
    window: Optional[MetricTimeWindow] = None,
    group_by: Optional[List[str]] = None,
    aggregation: str = "avg",
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> List[MetricSeries]:
    """
    Query metric data filtered by resource labels/dimensions using Datadog.

    Calls Datadog GET /api/v1/query endpoint via datadog_api_client SDK,
    applying dimension filters as Datadog tags and optionally grouping by
    specified dimensions.

    Args:
        metric_name: Datadog metric name, e.g. 'aws.ec2.cpuutilization'
        dimension_filters: List of DimensionFilter to apply as Datadog tag filters.
        window: Time window; defaults to last 60 minutes.
        group_by: Optional list of dimension keys to group results by.
        aggregation: Aggregation function (avg, sum, min, max, count, last).
        api_key: Datadog API key (or set DATADOG_API_KEY env var).
        app_key: Datadog App key (or set DATADOG_APP_KEY env var).

    Returns:
        List of MetricSeries, each representing data for a distinct dimension combination.
    """
    if window is None:
        window = MetricTimeWindow.from_now(minutes_ago=60)

    tags = build_datadog_tag_filter(dimension_filters)

    client = ObservabilityClient(api_key=api_key, app_key=app_key)
    try:
        metrics_api: MetricsApi = client.get_v1_api()

        # Build Datadog query string with tags and group_by
        base_query = f"{aggregation}:{metric_name}"
        if tags:
            tag_parts = [f"{k}:{v}" for k, v in tags.items()]
            base_query += "{" + ",".join(tag_parts) + "}"
        if group_by:
            base_query += f" by {{{','.join(group_by)}}}"

        start_ts = int(window.start.timestamp())
        end_ts = int(window.end.timestamp())

        # Call Datadog Metrics API
        raw_response = metrics_api.query_metrics(
            _from=start_ts,
            to=end_ts,
            query=base_query,
        )

        # Parse response into MetricSeries objects, grouped by scope/tags
        series_dict: Dict[str, MetricSeries] = {}
        series_list = raw_response.get("series", [])

        for series in series_list:
            expression = series.get("expression", "")
            scope = series.get("scope", "")
            series_key = scope or expression
            pointlist = series.get("pointlist", [])

            data_points: List[MetricDataPoint] = []
            for pt in pointlist:
                if len(pt) >= 2 and pt[1] is not None:
                    ts = datetime.utcfromtimestamp(pt[0] / 1000.0)
                    data_points.append(MetricDataPoint(
                        timestamp=ts,
                        value=float(pt[1]),
                        tags={"expression": expression, "scope": scope},
                    ))

            ms = MetricSeries(
                expression=expression,
                scope=scope,
                data_points=data_points,
            )
            series_dict[series_key] = ms

        return list(series_dict.values())
    finally:
        client.close()


def get_unique_dimension_values(
    metric_name: str,
    dimension_key: str,
    minutes_ago: int = 1440,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> List[str]:
    """
    Get unique values for a specific dimension key from a metric.

    Queries Datadog and extracts distinct tag values for the given dimension.
    """
    window = MetricTimeWindow.from_now(minutes_ago=minutes_ago)
    filters = [DimensionFilter(dimension_key=dimension_key, dimension_values=["*"], operator="exists")]
    series_list = filter_metric_dimensions(
        metric_name=metric_name,
        dimension_filters=filters,
        window=window,
        group_by=[dimension_key],
        api_key=api_key,
        app_key=app_key,
    )
    unique_values: List[str] = []
    for series in series_list:
        if series.scope:
            # Extract value from scope like "role:web,env:production"
            for part in series.scope.split(","):
                if part.startswith(f"{dimension_key}:"):
                    val = part.split(":", 1)[1]
                    if val not in unique_values:
                        unique_values.append(val)
    return unique_values
