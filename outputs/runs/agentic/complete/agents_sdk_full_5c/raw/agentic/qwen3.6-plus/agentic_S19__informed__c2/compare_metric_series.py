"""
Compare metric values for two resources or dimension filters over the same window
using Datadog Metrics API.

Queries two separate metric series from Datadog and computes comparison statistics.
Provider: Datadog (DD_API_KEY, DD_APP_KEY).
"""

from datetime import datetime, timezone
from typing import Optional

from observability_client import (
    create_datadog_session,
    build_datadog_query_url,
    build_time_window,
    normalize_metric_name,
)
from observability_models import (
    MetricSeries,
    MetricComparison,
    MetricAggregation,
    parse_datadog_query_response,
    compute_aggregation,
)

DATADOG_QUERY_ENDPOINT = "https://api.datadoghq.com/api/v1/query"


def _query_single_series(
    session,
    url: str,
    query_str: str,
    from_ts: int,
    to_ts: int,
    aggregator: str = "avg",
) -> MetricSeries:
    """Query a single metric series from Datadog."""
    params = {
        "query": query_str,
        "from": from_ts,
        "to": to_ts,
        "aggregator": aggregator,
    }
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    series_list = parse_datadog_query_response(data)
    if series_list:
        return series_list[0]
    return MetricSeries(metric=query_str.split("{")[0])


def compare_metric_series(
    metric_name: str,
    series_a_dimensions: dict[str, str],
    series_b_dimensions: dict[str, str],
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    window_minutes: int = 60,
) -> MetricComparison:
    """
    Compare metric values for two dimension filter sets from Datadog.

    Args:
        metric_name: Datadog metric name to compare.
        series_a_dimensions: Dimension filters for series A.
        series_b_dimensions: Dimension filters for series B.
        from_ts: Optional start epoch seconds.
        to_ts: Optional end epoch seconds.
        window_minutes: Window duration in minutes.

    Returns:
        MetricComparison with delta and correlation statistics.
    """
    normalized = normalize_metric_name(metric_name)
    start, end = build_time_window(window_minutes)
    if from_ts is not None:
        start = from_ts
    if to_ts is not None:
        end = to_ts

    tag_clause_a = ",".join(f"{k}:{v}" for k, v in series_a_dimensions.items())
    tag_clause_b = ",".join(f"{k}:{v}" for k, v in series_b_dimensions.items())
    query_a = f"{normalized}{{{tag_clause_a}}}"
    query_b = f"{normalized}{{{tag_clause_b}}}"

    session = create_datadog_session()
    url = build_datadog_query_url()

    series_a = _query_single_series(session, url, query_a, start, end)
    series_b = _query_single_series(session, url, query_b, start, end)

    agg_a = compute_aggregation(series_a)
    agg_b = compute_aggregation(series_b)

    delta_avg = agg_a.avg - agg_b.avg
    delta_max = agg_a.max_val - agg_b.max_val
    delta_min = agg_a.min_val - agg_b.min_val

    correlation = _compute_correlation(series_a.values, series_b.values)

    overlap = _compute_overlap(series_a.timestamps, series_b.timestamps)

    return MetricComparison(
        series_a=series_a,
        series_b=series_b,
        delta_avg=delta_avg,
        delta_max=delta_max,
        delta_min=delta_min,
        correlation=correlation,
        overlap_pct=overlap,
    )


def compare_metrics_by_name(
    metric_a: str,
    metric_b: str,
    common_dimensions: Optional[dict[str, str]] = None,
    from_ts: Optional[int] = None,
    to_ts: Optional[int] = None,
    window_minutes: int = 60,
) -> MetricComparison:
    """
    Compare two different metric names with optional common dimension filters from Datadog.

    Args:
        metric_a: First Datadog metric name.
        metric_b: Second Datadog metric name.
        common_dimensions: Optional shared dimension filters.
        from_ts: Optional start epoch seconds.
        to_ts: Optional end epoch seconds.
        window_minutes: Window duration in minutes.

    Returns:
        MetricComparison with statistics.
    """
    norm_a = normalize_metric_name(metric_a)
    norm_b = normalize_metric_name(metric_b)
    start, end = build_time_window(window_minutes)
    if from_ts is not None:
        start = from_ts
    if to_ts is not None:
        end = to_ts

    tag_clause = ""
    if common_dimensions:
        tag_clause = ",".join(f"{k}:{v}" for k, v in common_dimensions.items())

    query_a = f"{norm_a}{{{tag_clause}}}"
    query_b = f"{norm_b}{{{tag_clause}}}"

    session = create_datadog_session()
    url = build_datadog_query_url()

    series_a = _query_single_series(session, url, query_a, start, end)
    series_b = _query_single_series(session, url, query_b, start, end)

    agg_a = compute_aggregation(series_a)
    agg_b = compute_aggregation(series_b)

    return MetricComparison(
        series_a=series_a,
        series_b=series_b,
        delta_avg=agg_a.avg - agg_b.avg,
        delta_max=agg_a.max_val - agg_b.max_val,
        delta_min=agg_a.min_val - agg_b.min_val,
        correlation=_compute_correlation(series_a.values, series_b.values),
        overlap_pct=_compute_overlap(series_a.timestamps, series_b.timestamps),
    )


def _compute_correlation(values_a: list[float], values_b: list[float]) -> float:
    """Compute Pearson correlation between two value lists."""
    n = min(len(values_a), len(values_b))
    if n < 2:
        return 0.0
    va = values_a[:n]
    vb = values_b[:n]
    mean_a = sum(va) / n
    mean_b = sum(vb) / n
    cov = sum((va[i] - mean_a) * (vb[i] - mean_b) for i in range(n)) / n
    std_a = (sum((v - mean_a) ** 2 for v in va) / n) ** 0.5
    std_b = (sum((v - mean_b) ** 2 for v in vb) / n) ** 0.5
    if std_a == 0 or std_b == 0:
        return 0.0
    return cov / (std_a * std_b)


def _compute_overlap(ts_a: list[datetime], ts_b: list[datetime]) -> float:
    """Compute percentage of overlapping timestamps between two series."""
    set_a = set(t.timestamp() for t in ts_a)
    set_b = set(t.timestamp() for t in ts_b)
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    if not union:
        return 0.0
    return len(intersection) / len(union)
