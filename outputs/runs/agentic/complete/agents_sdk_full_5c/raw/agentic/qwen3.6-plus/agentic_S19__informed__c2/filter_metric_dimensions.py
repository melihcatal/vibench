"""
Query metric data filtered by resource labels or dimensions using Datadog Metrics API.

Uses the Datadog v1 Query API to retrieve metric time series filtered by
specific dimension/tag combinations. Provider: Datadog (DD_API_KEY, DD_APP_KEY).
"""

from typing import Optional

from observability_client import (
    create_datadog_session,
    build_datadog_query_url,
    build_time_window,
    normalize_metric_name,
)
from observability_models import (
    MetricSeries,
    MetricDataPoint,
    parse_datadog_query_response,
)

DATADOG_QUERY_ENDPOINT = "https://api.datadoghq.com/api/v1/query"


def filter_metric_dimensions(
    metric_name: str,
    dimension_filters: dict[str, str],
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    window_minutes: int = 60,
    aggregator: str = "avg",
) -> list[MetricSeries]:
    """
    Query metric data filtered by resource labels/dimensions from Datadog.

    Args:
        metric_name: Datadog metric name.
        dimension_filters: Dict of dimension key-value pairs to filter by
            (e.g., {"env": "production", "region": "us-east-1"}).
        from_ts: Optional start epoch seconds.
        to_ts: Optional end epoch seconds.
        window_minutes: Window duration in minutes.
        aggregator: Aggregation function.

    Returns:
        List of MetricSeries matching the dimension filters.
    """
    normalized = normalize_metric_name(metric_name)
    start, end = build_time_window(window_minutes)
    if from_ts is not None:
        start = from_ts
    if to_ts is not None:
        end = to_ts

    tag_parts = [f"{k}:{v}" for k, v in dimension_filters.items()]
    tag_clause = ",".join(tag_parts)
    query_str = f"{normalized}{{{tag_clause}}}"

    session = create_datadog_session()
    url = build_datadog_query_url()

    params = {
        "query": query_str,
        "from": start,
        "to": end,
        "aggregator": aggregator,
    }

    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    return parse_datadog_query_response(data)


def filter_metric_dimensions_with_wildcard(
    metric_name: str,
    required_dimensions: dict[str, str],
    optional_dimensions: Optional[dict[str, list[str]]] = None,
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    window_minutes: int = 60,
) -> list[MetricSeries]:
    """
    Query metric data with required and optional dimension filters from Datadog.

    Supports wildcard matching for optional dimensions.

    Args:
        metric_name: Datadog metric name.
        required_dimensions: Dimensions that must match exactly.
        optional_dimensions: Dimensions with multiple allowed values.
        from_ts: Optional start epoch seconds.
        to_ts: Optional end epoch seconds.
        window_minutes: Window duration in minutes.

    Returns:
        List of MetricSeries matching the filter criteria.
    """
    normalized = normalize_metric_name(metric_name)
    start, end = build_time_window(window_minutes)
    if from_ts is not None:
        start = from_ts
    if to_ts is not None:
        end = to_ts

    all_series = []

    if optional_dimensions:
        import itertools
        dimension_keys = list(optional_dimensions.keys())
        dimension_values = list(optional_dimensions.values())
        combinations = list(itertools.product(*dimension_values))

        for combo in combinations:
            tag_parts = [f"{k}:{v}" for k, v in required_dimensions.items()]
            for i, key in enumerate(dimension_keys):
                tag_parts.append(f"{key}:{combo[i]}")
            tag_clause = ",".join(tag_parts)
            query_str = f"{normalized}{{{tag_clause}}}"

            session = create_datadog_session()
            url = build_datadog_query_url()
            params = {
                "query": query_str,
                "from": start,
                "to": end,
                "aggregator": "avg",
            }

            response = session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            series_list = parse_datadog_query_response(data)
            all_series.extend(series_list)
    else:
        tag_parts = [f"{k}:{v}" for k, v in required_dimensions.items()]
        tag_clause = ",".join(tag_parts)
        query_str = f"{normalized}{{{tag_clause}}}"

        session = create_datadog_session()
        url = build_datadog_query_url()
        params = {
            "query": query_str,
            "from": start,
            "to": end,
            "aggregator": "avg",
        }

        response = session.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        all_series = parse_datadog_query_response(data)

    return all_series
