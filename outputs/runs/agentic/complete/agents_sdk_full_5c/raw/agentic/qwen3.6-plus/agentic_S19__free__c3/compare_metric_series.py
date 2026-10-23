"""
compare_metric_series.py
Compares metric values for two resources or dimension filters over the same window
using the Datadog API.
Provider: Datadog (api.datadoghq.com)
"""

import os
import math
from typing import List, Optional, Dict, Any, Tuple

from observability_client import get_metrics_api_v1, load_datadog_config
from observability_models import (
    MetricQueryRequest,
    MetricSeries,
    MetricComparisonResult,
    Datapoint,
    normalize_datadog_series_to_metric_series,
)


def compare_metric_series(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    filter_a: Optional[Dict[str, str]] = None,
    filter_b: Optional[Dict[str, str]] = None,
    tag_filter_a: Optional[List[str]] = None,
    tag_filter_b: Optional[List[str]] = None,
    aggregation: str = "avg",
) -> MetricComparisonResult:
    """
    Compare metric values between two resources or dimension sets via Datadog API.

    Fetches time series for both filter sets over the same time window and
    computes correlation, mean difference, and statistical comparison.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        filter_a: Dimension filters for series A, e.g. {"host": "web-01"}.
        filter_b: Dimension filters for series B, e.g. {"host": "web-02"}.
        tag_filter_a: Optional raw Datadog tag filters for series A.
        tag_filter_b: Optional raw Datadog tag filters for series B.
        aggregation: Aggregation function.

    Returns:
        MetricComparisonResult with statistical comparison metrics.
    """
    result = MetricComparisonResult(
        series_a_name=_build_filter_name(metric_name, filter_a, tag_filter_a),
        series_b_name=_build_filter_name(metric_name, filter_b, tag_filter_b),
        comparison_window=(start_ts, end_ts),
    )

    # Query series A
    series_a = _query_filtered_metric(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        dimension_filters=filter_a,
        tag_filters=tag_filter_a,
        aggregation=aggregation,
    )

    # Query series B
    series_b = _query_filtered_metric(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        dimension_filters=filter_b,
        tag_filters=tag_filter_b,
        aggregation=aggregation,
    )

    if series_a:
        result.series_a = series_a[0] if len(series_a) == 1 else _merge_series(series_a)
    if series_b:
        result.series_b = series_b[0] if len(series_b) == 1 else _merge_series(series_b)

    result.correlation = compute_correlation(result.series_a, result.series_b)
    result.mean_diff = compute_mean_difference(result.series_a, result.series_b)
    result.std_diff = compute_std_difference(result.series_a, result.series_b)
    result.overlap_pct = compute_value_overlap(result.series_a, result.series_b)

    return result


def compare_metric_trend(
    metric_name: str,
    current_start_ts: float,
    current_end_ts: float,
    previous_start_ts: float,
    previous_end_ts: float,
    tags: Optional[List[str]] = None,
    aggregation: str = "avg",
) -> MetricComparisonResult:
    """
    Compare current vs previous metric trend windows from Datadog.

    Args:
        metric_name: The Datadog metric name.
        current_start_ts: Current window start.
        current_end_ts: Current window end.
        previous_start_ts: Previous window start.
        previous_end_ts: Previous window end.
        tags: Optional tag filters applied to both windows.
        aggregation: Aggregation function.

    Returns:
        MetricComparisonResult comparing current vs previous period.
    """
    series_current = _query_filtered_metric(
        metric_name=metric_name,
        start_ts=current_start_ts,
        end_ts=current_end_ts,
        tag_filters=tags,
        aggregation=aggregation,
    )

    series_previous = _query_filtered_metric(
        metric_name=metric_name,
        start_ts=previous_start_ts,
        end_ts=previous_end_ts,
        tag_filters=tags,
        aggregation=aggregation,
    )

    result = MetricComparisonResult(
        series_a_name=f"{metric_name} (current)",
        series_b_name=f"{metric_name} (previous)",
        comparison_window=(previous_start_ts, current_end_ts),
    )

    if series_current:
        result.series_a = _merge_series(series_current) if len(series_current) > 1 else series_current[0]
    if series_previous:
        result.series_b = _merge_series(series_previous) if len(series_previous) > 1 else series_previous[0]

    result.mean_diff = compute_mean_difference(result.series_a, result.series_b)
    result.std_diff = compute_std_difference(result.series_a, result.series_b)

    return result


def compare_hosts_metric(
    metric_name: str,
    host_a: str,
    host_b: str,
    start_ts: float,
    end_ts: float,
    aggregation: str = "avg",
) -> MetricComparisonResult:
    """
    Compare a metric between two specific hosts via Datadog.

    Args:
        metric_name: The Datadog metric name.
        host_a: First host name.
        host_b: Second host name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        aggregation: Aggregation function.

    Returns:
        MetricComparisonResult for the two hosts.
    """
    return compare_metric_series(
        metric_name=metric_name,
        start_ts=start_ts,
        end_ts=end_ts,
        filter_a={"host": host_a},
        filter_b={"host": host_b},
        aggregation=aggregation,
    )


def _query_filtered_metric(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    dimension_filters: Optional[Dict[str, str]] = None,
    tag_filters: Optional[List[str]] = None,
    aggregation: str = "avg",
) -> List[MetricSeries]:
    """Query a single filtered metric series from Datadog."""
    all_tags = []
    if dimension_filters:
        for key, value in dimension_filters.items():
            all_tags.append(f"{key}:{value}")
    if tag_filters:
        all_tags.extend(tag_filters)

    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_ts,
        end_time=end_ts,
        aggregation=aggregation,
        tag_filters=all_tags if all_tags else None,
    )

    query_string = request.to_datadog_query()
    configuration = load_datadog_config()
    api = get_metrics_api_v1(configuration)
    api_client = api.api_client

    raw_response = api_client.call_api(
        resource_path="/api/v1/query",
        method="GET",
        query_params={
            "from": int(start_ts),
            "to": int(end_ts),
            "query": query_string,
        },
        response_type=dict,
    )

    if isinstance(raw_response, tuple):
        raw_response = raw_response[0]

    series_results = []
    for raw_series in raw_response.get("series", []):
        metric_series = normalize_datadog_series_to_metric_series(
            raw_series=raw_series,
            metric_name=metric_name,
            start_time=start_ts,
            end_time=end_ts,
        )
        series_results.append(metric_series)

    return series_results


def _build_filter_name(
    metric_name: str,
    filters: Optional[Dict[str, str]] = None,
    tags: Optional[List[str]] = None,
) -> str:
    """Build a descriptive name for a filtered series."""
    parts = [metric_name]
    if filters:
        for k, v in filters.items():
            parts.append(f"{k}={v}")
    if tags:
        parts.extend(tags)
    return " | ".join(parts)


def _merge_series(series_list: List[MetricSeries]) -> MetricSeries:
    """Merge multiple series into one by averaging overlapping points."""
    if not series_list:
        raise ValueError("Cannot merge empty series list")
    if len(series_list) == 1:
        return series_list[0]

    all_points: Dict[float, List[float]] = {}
    for series in series_list:
        for dp in series.datapoints:
            if dp.value is not None:
                if dp.timestamp not in all_points:
                    all_points[dp.timestamp] = []
                all_points[dp.timestamp].append(dp.value)

    merged_datapoints = []
    for ts in sorted(all_points.keys()):
        values = all_points[ts]
        avg_val = sum(values) / len(values)
        merged_datapoints.append(Datapoint(
            timestamp=ts,
            value=avg_val,
            metric_name=series_list[0].metric_name,
        ))

    return MetricSeries(
        metric_name=series_list[0].metric_name,
        display_name=series_list[0].display_name,
        datapoints=merged_datapoints,
        start_time=series_list[0].start_time,
        end_time=series_list[-1].end_time,
        aggregation=series_list[0].aggregation,
    )


def compute_correlation(series_a: Optional[MetricSeries], series_b: Optional[MetricSeries]) -> Optional[float]:
    """Compute Pearson correlation between two metric series."""
    if not series_a or not series_b:
        return None

    values_a = series_a.values()
    values_b = series_b.values()
    min_len = min(len(values_a), len(values_b))
    if min_len < 2:
        return None

    paired = [
        (values_a[i], values_b[i])
        for i in range(min_len)
        if values_a[i] is not None and values_b[i] is not None
    ]

    if len(paired) < 2:
        return None

    a_vals = [p[0] for p in paired]
    b_vals = [p[1] for p in paired]

    mean_a = sum(a_vals) / len(a_vals)
    mean_b = sum(b_vals) / len(b_vals)

    numerator = sum((a - mean_a) * (b - mean_b) for a, b in paired)
    denom_a = math.sqrt(sum((a - mean_a) ** 2 for a in a_vals))
    denom_b = math.sqrt(sum((b - mean_b) ** 2 for b in b_vals))

    if denom_a == 0 or denom_b == 0:
        return None

    return round(numerator / (denom_a * denom_b), 4)


def compute_mean_difference(
    series_a: Optional[MetricSeries],
    series_b: Optional[MetricSeries],
) -> Optional[float]:
    """Compute mean difference between two metric series."""
    if not series_a or not series_b:
        return None

    vals_a = series_a.non_null_values()
    vals_b = series_b.non_null_values()

    if not vals_a or not vals_b:
        return None

    return round(sum(vals_a) / len(vals_a) - sum(vals_b) / len(vals_b), 4)


def compute_std_difference(
    series_a: Optional[MetricSeries],
    series_b: Optional[MetricSeries],
) -> Optional[float]:
    """Compute standard deviation difference between two metric series."""
    if not series_a or not series_b:
        return None

    vals_a = series_a.non_null_values()
    vals_b = series_b.non_null_values()

    if len(vals_a) < 2 or len(vals_b) < 2:
        return None

    mean_a = sum(vals_a) / len(vals_a)
    mean_b = sum(vals_b) / len(vals_b)

    std_a = math.sqrt(sum((v - mean_a) ** 2 for v in vals_a) / (len(vals_a) - 1))
    std_b = math.sqrt(sum((v - mean_b) ** 2 for v in vals_b) / (len(vals_b) - 1))

    return round(std_a - std_b, 4)


def compute_value_overlap(
    series_a: Optional[MetricSeries],
    series_b: Optional[MetricSeries],
) -> Optional[float]:
    """Compute percentage overlap in value ranges between two series."""
    if not series_a or not series_b:
        return None

    vals_a = series_a.non_null_values()
    vals_b = series_b.non_null_values()

    if not vals_a or not vals_b:
        return None

    range_a = (min(vals_a), max(vals_a))
    range_b = (min(vals_b), max(vals_b))

    overlap_start = max(range_a[0], range_b[0])
    overlap_end = min(range_a[1], range_b[1])

    if overlap_start > overlap_end:
        return 0.0

    overlap = overlap_end - overlap_start
    total_range = max(range_a[1], range_b[1]) - min(range_a[0], range_b[0])

    if total_range == 0:
        return 100.0

    return round((overlap / total_range) * 100.0, 2)
