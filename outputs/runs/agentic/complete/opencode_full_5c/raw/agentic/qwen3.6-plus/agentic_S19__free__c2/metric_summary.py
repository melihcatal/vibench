from __future__ import annotations

from typing import List, Optional

from observability_client import ObservabilityClient, create_client
from observability_models import (
    MetricQueryRequest,
    MetricSummary,
    MetricTimeSeries,
    normalize_datadog_series,
)


def metric_summary(
    metric_name: str,
    start: int,
    end: int,
    tags: Optional[List[str]] = None,
    interval: Optional[int] = None,
    client: Optional[ObservabilityClient] = None,
) -> MetricSummary:
    if client is None:
        client = create_client()

    request = MetricQueryRequest(
        metric_name=metric_name,
        start=start,
        end=end,
        interval=interval,
        tags=tags,
    )

    query_str = request.to_datadog_query()
    params = request.to_datadog_params()

    response = client.query_metrics_v1(
        query=query_str,
        start=params["from"],
        end=params["to"],
        interval=params.get("interval"),
    )

    series_list = []
    for raw_series in response.get("series", []):
        series_list.append(normalize_datadog_series(raw_series, metric_name))

    if not series_list:
        return MetricSummary(
            metric_name=metric_name,
            time_window_start=start,
            time_window_end=end,
            summary_text=f"No data found for metric {metric_name} in the specified window.",
        )

    primary_series = series_list[0]
    points = primary_series.points

    if not points:
        return MetricSummary(
            metric_name=metric_name,
            time_window_start=start,
            time_window_end=end,
            summary_text=f"No datapoints found for metric {metric_name} in the specified window.",
        )

    sorted_points = sorted(points, key=lambda p: p.timestamp)
    values = [p.value for p in sorted_points]

    current_value = values[-1]
    previous_value = values[0] if len(values) > 1 else current_value

    percent_change = None
    if previous_value != 0:
        percent_change = ((current_value - previous_value) / abs(previous_value)) * 100

    trend_direction, trend_magnitude = _compute_trend(values)

    anomaly_detected, anomaly_score, anomaly_details = _detect_anomalies(sorted_points)

    summary_parts = [
        f"Metric: {metric_name}",
        f"Window: {start} to {end}",
        f"Current value: {current_value:.4f}",
        f"Previous value: {previous_value:.4f}",
    ]
    if percent_change is not None:
        summary_parts.append(f"Change: {percent_change:+.2f}%")
    if trend_direction:
        summary_parts.append(
            f"Trend: {trend_direction} (magnitude: {trend_magnitude:.4f})"
        )
    if anomaly_detected:
        summary_parts.append(f"Anomaly detected (score: {anomaly_score:.4f})")
        if anomaly_details:
            summary_parts.append(f"Details: {anomaly_details}")

    summary_text = " | ".join(summary_parts)

    return MetricSummary(
        metric_name=metric_name,
        time_window_start=start,
        time_window_end=end,
        current_value=current_value,
        previous_value=previous_value,
        trend_direction=trend_direction,
        trend_magnitude=trend_magnitude,
        anomaly_detected=anomaly_detected,
        anomaly_score=anomaly_score,
        anomaly_details=anomaly_details,
        percent_change=percent_change,
        series=primary_series,
        summary_text=summary_text,
    )


def _compute_trend(values: List[float]):
    if len(values) < 2:
        return None, None

    n = len(values)
    mean_x = (n - 1) / 2.0
    mean_y = sum(values) / n

    numerator = sum((i - mean_x) * (values[i] - mean_y) for i in range(n))
    denominator = sum((i - mean_x) ** 2 for i in range(n))

    if denominator == 0:
        return "flat", 0.0

    slope = numerator / denominator
    normalized_slope = slope / (mean_y if mean_y != 0 else 1.0)

    if abs(normalized_slope) < 0.01:
        direction = "flat"
    elif normalized_slope > 0:
        direction = "increasing"
    else:
        direction = "decreasing"

    return direction, abs(normalized_slope)


def _detect_anomalies(points: list):
    if len(points) < 3:
        return False, None, None

    values = [p.value for p in points]
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std_dev = variance**0.5

    if std_dev == 0:
        return False, None, None

    anomalies = []
    for i, p in enumerate(points):
        z_score = abs(p.value - mean) / std_dev
        if z_score > 2.0:
            anomalies.append((i, p.value, z_score))

    if anomalies:
        max_anomaly = max(anomalies, key=lambda a: a[2])
        anomaly_score = max_anomaly[2] / 3.0
        anomaly_score = min(anomaly_score, 1.0)
        detail = f"Found {len(anomalies)} anomalous point(s), max z-score: {max_anomaly[2]:.2f}"
        return True, anomaly_score, detail

    return False, None, None
