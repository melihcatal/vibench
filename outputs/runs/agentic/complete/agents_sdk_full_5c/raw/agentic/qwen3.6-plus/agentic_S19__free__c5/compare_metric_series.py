"""
Compare metric values for two resources or dimension filters over the same window.
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
    MetricComparisonResult,
    MetricQueryResponse,
    MetricSeries,
    parse_datadog_response_to_model,
)


def compare_metric_series(
    metric_name: str,
    dimensions_a: Dict[str, str],
    dimensions_b: Dict[str, str],
    minutes_ago: Optional[int] = None,
    hours_ago: Optional[int] = None,
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
    aggregation: str = "avg",
) -> MetricComparisonResult:
    """
    Compare metric values for two sets of resource labels/dimensions over the same
    time window using the Datadog Metrics API.

    Args:
        metric_name: The Datadog metric name (e.g. 'system.cpu.user').
        dimensions_a: Tag filters for series A (e.g. {"host": "web-01"}).
        dimensions_b: Tag filters for series B (e.g. {"host": "web-02"}).
        minutes_ago: How many minutes back to query.
        hours_ago: How many hours back to query.
        start_ts: Explicit start timestamp (epoch seconds).
        end_ts: Explicit end timestamp (epoch seconds).
        aggregation: Datadog aggregation function.

    Returns:
        MetricComparisonResult with statistics comparing the two series.
    """
    from_ts, to_ts = build_time_window(
        minutes_ago=minutes_ago,
        hours_ago=hours_ago,
        start_ts=start_ts,
        end_ts=end_ts,
    )

    query_a = build_metric_query_string(
        metric_name=metric_name,
        aggregation=aggregation,
        filter_tags=dimensions_a,
    )
    query_b = build_metric_query_string(
        metric_name=metric_name,
        aggregation=aggregation,
        filter_tags=dimensions_b,
    )

    metrics_api = get_metrics_api_client()

    raw_a = metrics_api.query_metrics(
        _from=from_ts,
        to=to_ts,
        query=query_a,
    )
    raw_b = metrics_api.query_metrics(
        _from=from_ts,
        to=to_ts,
        query=query_b,
    )

    parsed_a = parse_datadog_response_to_model(raw_a)
    parsed_b = parse_datadog_response_to_model(raw_b)

    values_a = _collect_all_values(parsed_a.series)
    values_b = _collect_all_values(parsed_b.series)

    series_a_name = _build_series_name(metric_name, dimensions_a)
    series_b_name = _build_series_name(metric_name, dimensions_b)

    avg_a = _safe_avg(values_a)
    avg_b = _safe_avg(values_b)
    abs_diff = abs(avg_a - avg_b)
    pct_diff = (abs_diff / avg_a * 100.0) if avg_a != 0 else 0.0

    return MetricComparisonResult(
        series_a_name=series_a_name,
        series_b_name=series_b_name,
        series_a_avg=avg_a,
        series_b_avg=avg_b,
        absolute_diff=abs_diff,
        percent_diff=pct_diff,
        series_a_max=max(values_a) if values_a else 0.0,
        series_b_max=max(values_b) if values_b else 0.0,
        series_a_min=min(values_a) if values_a else 0.0,
        series_b_min=min(values_b) if values_b else 0.0,
        series_a_count=len(values_a),
        series_b_count=len(values_b),
        start_ts=from_ts,
        end_ts=to_ts,
    )


def compare_metric_series_dict(
    metric_name: str,
    dimensions_a: Dict[str, str],
    dimensions_b: Dict[str, str],
    minutes_ago: int = 60,
    aggregation: str = "avg",
) -> Dict[str, Any]:
    """
    Convenience wrapper that returns comparison result as a dict.

    Args:
        metric_name: The Datadog metric name.
        dimensions_a: Tag filters for series A.
        dimensions_b: Tag filters for series B.
        minutes_ago: Window in minutes.
        aggregation: Aggregation function.

    Returns:
        Dict representation of the comparison result.
    """
    result = compare_metric_series(
        metric_name=metric_name,
        dimensions_a=dimensions_a,
        dimensions_b=dimensions_b,
        minutes_ago=minutes_ago,
        aggregation=aggregation,
    )
    return result.to_dict()


def _collect_all_values(series_list: List[MetricSeries]) -> List[float]:
    """Collect all point values from a list of series."""
    values = []
    for series in series_list:
        values.extend(series.values())
    return values


def _safe_avg(values: List[float]) -> float:
    """Compute average safely, returning 0.0 for empty lists."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def _build_series_name(metric_name: str, dimensions: Dict[str, str]) -> str:
    """Build a human-readable series name from metric name and dimensions."""
    if not dimensions:
        return metric_name
    tag_str = ",".join(f"{k}={v}" for k, v in sorted(dimensions.items()))
    return f"{metric_name}{{{tag_str}}}"
