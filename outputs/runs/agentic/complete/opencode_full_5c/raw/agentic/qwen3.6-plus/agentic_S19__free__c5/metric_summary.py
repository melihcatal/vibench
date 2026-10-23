from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

from observability_client import (
    DATADOG_API_BASE,
    create_datadog_session,
    validate_datadog_credentials,
)
from observability_models import (
    MetricDataPoint,
    MetricSummary,
    normalize_datadog_response,
)


def _detect_anomalies(
    data_points: List[MetricDataPoint],
    z_threshold: float = 2.0,
) -> List[MetricDataPoint]:
    if len(data_points) < 3:
        return []

    values = [dp.value for dp in data_points]
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std_dev = variance**0.5

    if std_dev == 0:
        return []

    anomalies = []
    for dp in data_points:
        z_score = abs(dp.value - mean) / std_dev
        if z_score > z_threshold:
            anomalies.append(dp)

    return anomalies


def _determine_trend(data_points: List[MetricDataPoint]) -> str:
    if len(data_points) < 2:
        return "stable"

    n = len(data_points)
    half = n // 2
    first_half = [dp.value for dp in data_points[:half]]
    second_half = [dp.value for dp in data_points[half:]]

    avg_first = sum(first_half) / len(first_half)
    avg_second = sum(second_half) / len(second_half)

    if avg_first == 0:
        return "stable"

    change_pct = (avg_second - avg_first) / abs(avg_first)

    if change_pct > 0.1:
        return "increasing"
    elif change_pct < -0.1:
        return "decreasing"
    else:
        return "stable"


def metric_summary(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    aggregation: str = "avg",
    dimensions: Optional[Dict[str, str]] = None,
    z_threshold: float = 2.0,
) -> MetricSummary:
    if not validate_datadog_credentials():
        raise ValueError(
            "Datadog credentials not configured. Set DATADOG_API_KEY and DATADOG_APP_KEY environment variables."
        )

    query = f"{aggregation}:{metric_name}"
    if dimensions:
        dim_parts = []
        for k, v in dimensions.items():
            dim_parts.append(f"{k}:{v}")
        query = f"{query}{{{' AND '.join(dim_parts)}}}"

    payload = {
        "query": query,
        "from": int(start_time.timestamp()),
        "to": int(end_time.timestamp()),
    }

    session = create_datadog_session()
    api_url = f"{DATADOG_API_BASE}/api/v1/query"

    response = session.get(api_url, params=payload, timeout=30)
    response.raise_for_status()

    raw_data = response.json()
    data_points = normalize_datadog_response(raw_data)

    if not data_points:
        return MetricSummary(
            metric_name=metric_name,
            period_start=start_time,
            period_end=end_time,
            current_value=0.0,
            previous_value=0.0,
            trend_direction="unknown",
            anomaly_detected=False,
            anomaly_score=0.0,
            summary_text=f"No data available for metric {metric_name} in the specified time window.",
            data_points_analyzed=0,
        )

    current_value = data_points[-1].value
    previous_value = data_points[0].value if len(data_points) > 1 else current_value

    trend_direction = _determine_trend(data_points)
    anomalies = _detect_anomalies(data_points, z_threshold)
    anomaly_detected = len(anomalies) > 0
    anomaly_score = len(anomalies) / len(data_points) if data_points else 0.0

    summary_parts = [
        f"Metric {metric_name} shows a {trend_direction} trend",
        f"over the period from {start_time.strftime('%Y-%m-%d %H:%M')} to {end_time.strftime('%Y-%m-%d %H:%M')}.",
        f"Current value: {current_value:.2f}, previous value: {previous_value:.2f}.",
    ]

    if anomaly_detected:
        summary_parts.append(
            f"Detected {len(anomalies)} anomalous data points "
            f"(anomaly score: {anomaly_score:.2f})."
        )
    else:
        summary_parts.append("No significant anomalies detected.")

    summary_text = " ".join(summary_parts)

    return MetricSummary(
        metric_name=metric_name,
        period_start=start_time,
        period_end=end_time,
        current_value=current_value,
        previous_value=previous_value,
        trend_direction=trend_direction,
        anomaly_detected=anomaly_detected,
        anomaly_score=anomaly_score,
        summary_text=summary_text,
        data_points_analyzed=len(data_points),
    )
