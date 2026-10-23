"""
Compare metric values for two resources or dimension filters over the same window.

Uses the Datadog Metrics API (api.datadoghq.com) to fetch two metric series
and compute statistical comparisons including diff, correlation, and divergence.
"""

import os
import math
import requests
from typing import Optional, Dict, Any, List, Tuple

from observability_client import (
    load_datadog_config,
    build_datadog_session,
    normalize_timestamps,
    format_datadog_query,
)
from observability_models import (
    MetricQueryResponse,
    MetricSeries,
    MetricDatapoint,
    MetricComparisonResult,
    parse_datadog_query_response,
    normalize_dimensions,
)


def _fetch_metric_series(
    session: requests.Session,
    metric_name: str,
    start_ts: int,
    end_ts: int,
    dimensions: Optional[Dict[str, str]],
    aggregation: str = "avg",
) -> MetricQueryResponse:
    """Internal helper to fetch a metric series from Datadog."""
    norm_dims = normalize_dimensions(dimensions) if dimensions else None
    query_str = format_datadog_query(
        metric_name=metric_name,
        rollup=aggregation,
        aggregation=aggregation,
        dimensions=norm_dims,
    )

    params = {
        "query": query_str,
        "from": start_ts,
        "to": end_ts,
    }

    api_url = f"{session.base_url}/api/v1/query"
    resp = session.get(api_url, params=params, timeout=30)
    resp.raise_for_status()

    raw_json = resp.json()
    return parse_datadog_query_response(raw_json)


def _align_series(
    series_a: List[MetricDatapoint],
    series_b: List[MetricDatapoint],
) -> Tuple[List[float], List[float]]:
    """Align two series by timestamp, returning paired values.

    Creates a union of timestamps and interpolates using nearest-neighbor
    for timestamps present in one series but not the other.

    Returns:
        Tuple of (values_a, values_b) with matching lengths.
    """
    ts_map_a = {dp.timestamp: dp.value for dp in series_a}
    ts_map_b = {dp.timestamp: dp.value for dp in series_b}

    all_timestamps = sorted(set(ts_map_a.keys()) | set(ts_map_b.keys()))
    if not all_timestamps:
        return [], []

    values_a = []
    values_b = []

    # Use nearest-neighbor interpolation for alignment
    for ts in all_timestamps:
        va = ts_map_a.get(ts)
        vb = ts_map_b.get(ts)

        if va is None:
            # Find nearest timestamp in series_a
            nearest = min(ts_map_a.keys(), key=lambda t: abs(t - ts)) if ts_map_a else None
            va = ts_map_a.get(nearest, 0.0) if nearest is not None else 0.0

        if vb is None:
            nearest = min(ts_map_b.keys(), key=lambda t: abs(t - ts)) if ts_map_b else None
            vb = ts_map_b.get(nearest, 0.0) if nearest is not None else 0.0

        values_a.append(va)
        values_b.append(vb)

    return values_a, values_b


def _compute_correlation(values_a: List[float], values_b: List[float]) -> float:
    """Compute Pearson correlation coefficient between two value lists."""
    n = len(values_a)
    if n < 2:
        return 0.0

    mean_a = sum(values_a) / n
    mean_b = sum(values_b) / n

    cov = sum((a - mean_a) * (b - mean_b) for a, b in zip(values_a, values_b))
    std_a = math.sqrt(sum((a - mean_a) ** 2 for a in values_a))
    std_b = math.sqrt(sum((b - mean_b) ** 2 for b in values_b))

    if std_a == 0 or std_b == 0:
        return 0.0

    return cov / (std_a * std_b)


def compare_metric_series(
    metric_name: str,
    start_ts: int,
    end_ts: int,
    dimensions_a: Dict[str, str],
    dimensions_b: Dict[str, str],
    aggregation: str = "avg",
    config: Optional[Dict[str, str]] = None,
) -> MetricComparisonResult:
    """Compare metric values for two resources or dimension filters over the same window.

    Queries the Datadog Metrics API twice (once per dimension set), aligns
    the resulting time series by timestamp, and computes diff statistics
    and Pearson correlation.

    Args:
        metric_name: The Datadog metric name, e.g., 'system.cpu.usage'.
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.
        dimensions_a: Tag filters for series A, e.g., {'host': 'web-1'}.
        dimensions_b: Tag filters for series B, e.g., {'host': 'web-2'}.
        aggregation: Aggregation function (avg, sum, min, max).
        config: Optional Datadog config dict; loaded from env if omitted.

    Returns:
        MetricComparisonResult with aligned diff and correlation.

    Raises:
        ValueError: If either dimensions dict is empty.
    """
    if not dimensions_a:
        raise ValueError("dimensions_a must be provided")
    if not dimensions_b:
        raise ValueError("dimensions_b must be provided")

    start_ts, end_ts = normalize_timestamps(start_ts, end_ts)

    if config is None:
        config = load_datadog_config()
    session = build_datadog_session(config)

    # Fetch both series
    resp_a = _fetch_metric_series(session, metric_name, start_ts, end_ts, dimensions_a, aggregation)
    resp_b = _fetch_metric_series(session, metric_name, start_ts, end_ts, dimensions_b, aggregation)

    # Extract primary series from each response
    series_a = resp_a.series[0] if resp_a.series else MetricSeries(metric_name=metric_name)
    series_b = resp_b.series[0] if resp_b.series else MetricSeries(metric_name=metric_name)

    # Align timestamps
    values_a, values_b = _align_series(series_a.datapoints, series_b.datapoints)

    # Compute differences
    diff_per_point = [a - b for a, b in zip(values_a, values_b)]

    result = MetricComparisonResult(
        series_a=series_a,
        series_b=series_b,
        diff_per_point=diff_per_point,
        mean_diff=sum(diff_per_point) / len(diff_per_point) if diff_per_point else 0.0,
        max_diff=max(diff_per_point) if diff_per_point else 0.0,
        min_diff=min(diff_per_point) if diff_per_point else 0.0,
    )

    # Compute correlation
    if len(values_a) >= 2:
        result.correlation = _compute_correlation(values_a, values_b)
        result.correlation_computed = True

    return result


def compare_metric_series_summary(
    metric_name: str,
    start_ts: int,
    end_ts: int,
    dimensions_a: Dict[str, str],
    dimensions_b: Dict[str, str],
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: str = "datadoghq.com",
    aggregation: str = "avg",
) -> Dict[str, Any]:
    """Compare two metric series and return a JSON-serializable summary.

    Convenience wrapper that returns a simple dict suitable for API responses.

    Args:
        metric_name: The metric to compare.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        dimensions_a: Tag filters for series A.
        dimensions_b: Tag filters for series B.
        api_key: Datadog DD_API_KEY.
        app_key: Datadog DD_APP_KEY.
        site: Datadog site hostname.
        aggregation: Aggregation function.

    Returns:
        Dict with comparison summary fields.
    """
    cfg = {
        "api_key": api_key or os.environ.get("DD_API_KEY", ""),
        "app_key": app_key or os.environ.get("DD_APP_KEY", ""),
        "site": site,
    }
    result = compare_metric_series(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        dimensions_a=dimensions_a,
        dimensions_b=dimensions_b,
        aggregation=aggregation,
        config=cfg,
    )

    return {
        "metric_name": metric_name,
        "series_a_tags": result.series_a.tags,
        "series_b_tags": result.series_b.tags,
        "data_points_compared": len(result.diff_per_point),
        "mean_diff": result.mean_diff,
        "max_diff": result.max_diff,
        "min_diff": result.min_diff,
        "correlation": result.correlation,
        "correlation_computed": result.correlation_computed,
    }
