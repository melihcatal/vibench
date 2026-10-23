"""
Query metric data filtered by resource labels or dimensions.
Uses the Datadog Metrics API (datadog_api_client) as the concrete provider.
Provider: Datadog (api.datadoghq.com)
"""

from typing import Optional, Dict, List, Any

from observability_client import (
    get_metrics_api_client,
    build_time_window,
    build_metric_query_string,
)
from observability_models import (
    MetricQueryResponse,
    MetricSeries,
    MetricDataPoint,
    parse_datadog_response_to_model,
)


def filter_metric_dimensions(
    metric_name: str,
    dimensions: Dict[str, str],
    minutes_ago: Optional[int] = None,
    hours_ago: Optional[int] = None,
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
    aggregation: str = "avg",
    rollup_interval: Optional[int] = None,
) -> MetricQueryResponse:
    """
    Query metric data filtered by resource labels or dimensions using Datadog.

    Datadog tags serve as dimensions for filtering. This function builds
    a tag-filtered query and returns the matching series.

    Args:
        metric_name: The Datadog metric name (e.g. 'aws.ec2.cpuutilization').
        dimensions: Dict of dimension key-value pairs mapped to Datadog tags
                    (e.g. {"host": "web-01", "env": "production"}).
        minutes_ago: How many minutes back to query.
        hours_ago: How many hours back to query.
        start_ts: Explicit start timestamp (epoch seconds).
        end_ts: Explicit end timestamp (epoch seconds).
        aggregation: Datadog aggregation function.
        rollup_interval: Optional rollup interval in seconds.

    Returns:
        MetricQueryResponse containing only the series matching the dimension filters.
    """
    from_ts, to_ts = build_time_window(
        minutes_ago=minutes_ago,
        hours_ago=hours_ago,
        start_ts=start_ts,
        end_ts=end_ts,
    )

    query_string = build_metric_query_string(
        metric_name=metric_name,
        aggregation=aggregation,
        filter_tags=dimensions,
        rollup_interval=rollup_interval,
    )

    metrics_api = get_metrics_api_client()

    raw_response = metrics_api.query_metrics(
        _from=from_ts,
        to=to_ts,
        query=query_string,
    )

    parsed = parse_datadog_response_to_model(raw_response)
    return parsed


def query_filtered_series_list(
    metric_name: str,
    dimensions: Dict[str, str],
    minutes_ago: int = 60,
    aggregation: str = "avg",
) -> List[Dict[str, Any]]:
    """
    Return a list of series summaries matching the given dimension filters.

    Args:
        metric_name: The Datadog metric name.
        dimensions: Dimension key-value pairs as Datadog tags.
        minutes_ago: Window in minutes.
        aggregation: Aggregation type.

    Returns:
        List of dicts with series metadata and point counts.
    """
    response = filter_metric_dimensions(
        metric_name=metric_name,
        dimensions=dimensions,
        minutes_ago=minutes_ago,
        aggregation=aggregation,
    )

    series_summaries = []
    for series in response.series:
        series_summaries.append({
            "metric": series.metric,
            "display_name": series.display_name,
            "scope": series.scope,
            "aggregation": series.aggregation,
            "unit": series.unit,
            "point_count": series.point_count,
        })
    return series_summaries


def get_dimension_values_for_metric(
    metric_name: str,
    dimension_tag_key: str,
    minutes_ago: int = 60,
) -> List[str]:
    """
    Discover distinct dimension values for a given tag key on a metric.

    Queries the metric without tag filters and extracts unique values
    from the scope strings in returned series.

    Args:
        metric_name: The Datadog metric name.
        dimension_tag_key: The tag key to extract values for (e.g. 'host', 'env').
        minutes_ago: Window in minutes.

    Returns:
        List of unique dimension values found in the series scopes.
    """
    response = filter_metric_dimensions(
        metric_name=metric_name,
        dimensions={},
        minutes_ago=minutes_ago,
    )

    values = set()
    tag_prefix = f"{dimension_tag_key}:"
    for series in response.series:
        if tag_prefix in series.scope:
            parts = series.scope.split(",")
            for part in parts:
                part = part.strip()
                if part.startswith(tag_prefix):
                    values.add(part[len(tag_prefix):])

    return sorted(values)
