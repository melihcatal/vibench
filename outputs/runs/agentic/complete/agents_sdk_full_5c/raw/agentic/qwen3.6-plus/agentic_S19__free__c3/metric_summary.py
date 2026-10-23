"""
metric_summary.py
Summarize recent metric trends or anomalies using Datadog API data.
Provider: Datadog (api.datadoghq.com)
"""

import os
import math
from typing import List, Optional, Dict, Any

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

from observability_client import get_metrics_api_v1, load_datadog_config
from observability_models import (
    MetricSummary,
    MetricSeries,
    Datapoint,
    normalize_datadog_series_to_metric_series,
)


def summarize_metric_trends(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    tags: Optional[List[str]] = None,
    anomaly_threshold_std: float = 2.0,
    aggregation: str = "avg",
) -> List[MetricSummary]:
    """
    Summarize recent metric trends and detect anomalies using Datadog data.

    Analyzes metric series from Datadog and identifies trends (increasing,
    decreasing, stable) along with anomalous data points based on standard
    deviation thresholds.

    Args:
        metric_name: The Datadog metric name.
        start_ts: Start epoch seconds.
        end_ts: End epoch seconds.
        tags: Optional tag filters.
        anomaly_threshold_std: Number of standard deviations for anomaly detection.
        aggregation: Aggregation function.

    Returns:
        List of MetricSummary objects describing trends and anomalies.
    """
    configuration = load_datadog_config()
    api = get_metrics_api_v1(configuration)
    api_client = api.api_client

    query_string = f"{aggregation}:{metric_name}"
    if tags:
        query_string += "{" + ",".join(tags) + "}"

    try:
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

        summaries = []
        for raw_series in raw_response.get("series", []):
            metric_series = normalize_datadog_series_to_metric_series(
                raw_series=raw_series,
                metric_name=metric_name,
                start_time=start_ts,
                end_time=end_ts,
            )
            summary = _analyze_series_for_trends(
                metric_series=metric_series,
                anomaly_threshold_std=anomaly_threshold_std,
            )
            summaries.append(summary)

        return summaries

    except Exception as exc:
        raise RuntimeError(
            f"Datadog metric_summary failed for metric '{metric_name}': {exc}"
        ) from exc


def detect_metric_anomalies(
    metric_name: str,
    lookback_seconds: int = 7200,
    threshold_std: float = 2.5,
    tags: Optional[List[str]] = None,
    aggregation: str = "avg",
) -> List[MetricSummary]:
    """
    Detect anomalous datapoints for a metric from Datadog.

    Uses a lookback window to establish a baseline and flags values that
    deviate beyond the specified standard deviation threshold.

    Args:
        metric_name: The Datadog metric name.
        lookback_seconds: How far back to look in seconds (default 2 hours).
        threshold_std: Anomaly threshold in standard deviations.
        tags: Optional tag filters.
        aggregation: Aggregation function.

    Returns:
        List of MetricSummary with anomaly details.
    """
    import time
    now = time.time()
    start = now - lookback_seconds

    return summarize_metric_trends(
        metric_name=metric_name,
        start_ts=start,
        end_ts=now,
        tags=tags,
        anomaly_threshold_std=threshold_std,
        aggregation=aggregation,
    )


def _analyze_series_for_trends(
    metric_series: MetricSeries,
    anomaly_threshold_std: float = 2.0,
) -> MetricSummary:
    """Analyze a single metric series for trends and anomalies."""
    values = metric_series.non_null_values()

    if not values:
        return MetricSummary(
            metric_name=metric_series.metric_name,
            window_start=metric_series.start_time,
            window_end=metric_series.end_time,
            trend="unknown",
            anomaly_count=0,
            anomaly_timestamps=[],
            current_value=None,
            baseline_value=None,
            deviation_pct=None,
        )

    count = len(values)
    mean_val = sum(values) / count
    variance = sum((v - mean_val) ** 2 for v in values) / max(count - 1, 1)
    std_val = variance ** 0.5

    # Detect trend using linear regression slope
    trend = _compute_trend(values, count)

    # Detect anomalies
    anomaly_timestamps = []
    if std_val > 0:
        for dp in metric_series.datapoints:
            if dp.value is not None and abs(dp.value - mean_val) > (anomaly_threshold_std * std_val):
                anomaly_timestamps.append(dp.timestamp)

    anomaly_timestamps.sort()

    # Current vs baseline
    current_value = values[-1] if values else None
    baseline_value = mean_val
    deviation_pct = None
    if baseline_value and baseline_value != 0:
        if current_value is not None:
            deviation_pct = round(((current_value - baseline_value) / abs(baseline_value)) * 100.0, 2)

    return MetricSummary(
        metric_name=metric_series.metric_name,
        window_start=metric_series.start_time,
        window_end=metric_series.end_time,
        trend=trend,
        anomaly_count=len(anomaly_timestamps),
        anomaly_timestamps=anomaly_timestamps,
        current_value=current_value,
        baseline_value=round(baseline_value, 4),
        deviation_pct=deviation_pct,
    )


def _compute_trend(values: List[float], count: int) -> str:
    """
    Compute trend direction using simple linear regression slope.

    Uses least-squares linear fit to determine if the series is
    increasing, decreasing, or stable.
    """
    if count < 3:
        return "unknown"

    n = float(count)
    x_vals = list(range(count))
    x_mean = sum(x_vals) / n
    y_mean = sum(values) / n

    numerator = sum((x_vals[i] - x_mean) * (values[i] - y_mean) for i in range(count))
    denominator = sum((x_vals[i] - x_mean) ** 2 for i in range(count))

    if denominator == 0:
        return "stable"

    slope = numerator / denominator

    # Normalize slope relative to mean value for thresholding
    if y_mean != 0:
        relative_slope = abs(slope / y_mean)
    else:
        relative_slope = abs(slope)

    if relative_slope < 0.001:
        return "stable"
    elif slope > 0:
        return "increasing"
    else:
        return "decreasing"
