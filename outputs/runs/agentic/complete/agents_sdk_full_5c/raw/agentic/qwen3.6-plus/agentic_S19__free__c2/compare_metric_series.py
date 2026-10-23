"""
Compares metric values for two resources or dimension filters over the same window.

Provider: Datadog Metrics API (datadog-api-client)
Uses datadog_api_client.v1.api.metrics_api.MetricsApi and the api.datadoghq.com endpoint.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi

from observability_client import ObservabilityClient
from observability_models import (
    DimensionFilter,
    MetricComparisonResult,
    MetricDataPoint,
    MetricSeries,
    MetricTimeWindow,
)


def _align_series_by_timestamp(
    series_a: MetricSeries, series_b: MetricSeries
) -> List[tuple]:
    """Align two series by timestamp for comparison, returning (ts, val_a, val_b) tuples."""
    ts_map_a: Dict[float, float] = {dp.timestamp.timestamp(): dp.value for dp in series_a.data_points}
    ts_map_b: Dict[float, float] = {dp.timestamp.timestamp(): dp.value for dp in series_b.data_points}

    all_timestamps = sorted(set(ts_map_a.keys()) | set(ts_map_b.keys()))
    aligned: List[tuple] = []
    for ts in all_timestamps:
        val_a = ts_map_a.get(ts)
        val_b = ts_map_b.get(ts)
        if val_a is not None and val_b is not None:
            aligned.append((ts, val_a, val_b))
    return aligned


def _compute_correlation(aligned: List[tuple]) -> Optional[float]:
    """Compute Pearson correlation coefficient for aligned data."""
    if len(aligned) < 2:
        return None
    vals_a = [x[1] for x in aligned]
    vals_b = [x[2] for x in aligned]
    n = len(vals_a)
    mean_a = sum(vals_a) / n
    mean_b = sum(vals_b) / n

    cov = sum((a - mean_a) * (b - mean_b) for a, b in zip(vals_a, vals_b)) / n
    std_a = (sum((a - mean_a) ** 2 for a in vals_a) / n) ** 0.5
    std_b = (sum((b - mean_b) ** 2 for b in vals_b) / n) ** 0.5

    if std_a == 0 or std_b == 0:
        return 0.0
    return cov / (std_a * std_b)


def _compute_mean_difference(aligned: List[tuple]) -> Optional[float]:
    """Compute mean of differences (a - b)."""
    if not aligned:
        return None
    diffs = [a - b for _, a, b in aligned]
    return sum(diffs) / len(diffs)


def _compute_relative_change_pct(aligned: List[tuple]) -> Optional[float]:
    """Compute average relative change of series_b vs series_a as percentage."""
    if not aligned:
        return None
    changes = []
    for _, val_a, val_b in aligned:
        if val_a != 0:
            changes.append((val_b - val_a) / abs(val_a) * 100)
    if not changes:
        return None
    return sum(changes) / len(changes)


def compare_metric_series(
    metric_name: str,
    filter_a: List[DimensionFilter],
    filter_b: List[DimensionFilter],
    window: Optional[MetricTimeWindow] = None,
    aggregation: str = "avg",
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> MetricComparisonResult:
    """
    Compare metric values for two resource/dimension filters using Datadog.

    Queries Datadog GET /api/v1/query twice via datadog_api_client SDK—once
    for each set of dimension filters—and computes correlation, mean difference,
    and relative change between the two series.

    Args:
        metric_name: Datadog metric name, e.g. 'system.cpu.usage'
        filter_a: First set of dimension filters (tags) to compare.
        filter_b: Second set of dimension filters (tags) to compare.
        window: Time window; defaults to last 60 minutes.
        aggregation: Aggregation function (avg, sum, min, max).
        api_key: Datadog API key (or set DATADOG_API_KEY env var).
        app_key: Datadog App key (or set DATADOG_APP_KEY env var).

    Returns:
        MetricComparisonResult with correlation, mean difference, and relative change.
    """
    if window is None:
        window = MetricTimeWindow.from_now(minutes_ago=60)

    # Build tag dicts for each filter set
    def build_tags(filters: List[DimensionFilter]) -> Dict[str, str]:
        tag_dict: Dict[str, str] = {}
        for f in filters:
            if f.operator == "in" and f.dimension_values:
                tag_dict[f.dimension_key] = f.dimension_values[0]
            elif f.operator == "exists":
                tag_dict[f.dimension_key] = "*"
        return tag_dict

    tags_a = build_tags(filter_a)
    tags_b = build_tags(filter_b)

    client = ObservabilityClient(api_key=api_key, app_key=app_key)
    try:
        metrics_api: MetricsApi = client.get_v1_api()
        start_ts = int(window.start.timestamp())
        end_ts = int(window.end.timestamp())

        # Query series A
        query_a = f"{aggregation}:{metric_name}"
        if tags_a:
            tag_parts = [f"{k}:{v}" for k, v in tags_a.items()]
            query_a += "{" + ",".join(tag_parts) + "}"

        raw_a = metrics_api.query_metrics(_from=start_ts, to=end_ts, query=query_a)

        # Query series B
        query_b = f"{aggregation}:{metric_name}"
        if tags_b:
            tag_parts = [f"{k}:{v}" for k, v in tags_b.items()]
            query_b += "{" + ",".join(tag_parts) + "}"

        raw_b = metrics_api.query_metrics(_from=start_ts, to=end_ts, query=query_b)

        # Parse responses
        def parse_series(raw_response: dict) -> MetricSeries:
            data_points: List[MetricDataPoint] = []
            series_list = raw_response.get("series", [])
            for series in series_list:
                expression = series.get("expression", "")
                scope = series.get("scope", "")
                for pt in series.get("pointlist", []):
                    if len(pt) >= 2 and pt[1] is not None:
                        ts = datetime.utcfromtimestamp(pt[0] / 1000.0)
                        data_points.append(MetricDataPoint(
                            timestamp=ts,
                            value=float(pt[1]),
                            tags={"expression": expression, "scope": scope},
                        ))
            expr = series_list[0].get("expression", query_a) if series_list else query_a
            scope = series_list[0].get("scope", "") if series_list else ""
            return MetricSeries(expression=expr, scope=scope, data_points=data_points)

        series_a = parse_series(raw_a)
        series_b = parse_series(raw_b)

        # Align and compute statistics
        aligned = _align_series_by_timestamp(series_a, series_b)
        correlation = _compute_correlation(aligned)
        mean_diff = _compute_mean_difference(aligned)
        rel_change = _compute_relative_change_pct(aligned)

        return MetricComparisonResult(
            series_a=series_a,
            series_b=series_b,
            correlation=correlation,
            mean_difference=mean_diff,
            relative_change_pct=rel_change,
        )
    finally:
        client.close()


def get_comparison_summary(
    metric_name: str,
    resource_a: str,
    resource_b: str,
    dimension_key: str = "host",
    minutes_ago: int = 60,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> Dict[str, any]:
    """
    Get a human-readable comparison summary between two resources.
    """
    window = MetricTimeWindow.from_now(minutes_ago=minutes_ago)
    filter_a = [DimensionFilter(dimension_key=dimension_key, dimension_values=[resource_a])]
    filter_b = [DimensionFilter(dimension_key=dimension_key, dimension_values=[resource_b])]

    result = compare_metric_series(
        metric_name=metric_name,
        filter_a=filter_a,
        filter_b=filter_b,
        window=window,
        api_key=api_key,
        app_key=app_key,
    )

    return {
        "metric": metric_name,
        "resource_a": resource_a,
        "resource_b": resource_b,
        "correlation": result.correlation,
        "mean_difference": result.mean_difference,
        "relative_change_pct": result.relative_change_pct,
        "points_a": len(result.series_a.data_points),
        "points_b": len(result.series_b.data_points),
    }
