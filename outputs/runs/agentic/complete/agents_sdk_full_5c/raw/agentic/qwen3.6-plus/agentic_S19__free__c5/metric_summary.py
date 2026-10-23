"""
Summarize recent metric trends or anomalies.
Uses the Datadog Metrics API (datadog_api_client) as the concrete provider.
Provider: Datadog (api.datadoghq.com)
"""

from typing import Optional, Dict, List, Any

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

from observability_client import (
    build_time_window,
    build_metric_query_string,
    normalize_datadog_metric_response,
)
from observability_models import (
    MetricTrendSummary,
    MetricDataPoint,
    MetricSeries,
    MetricQueryResponse,
    parse_datadog_response_to_model,
)


def metric_summary(
    metric_name: str,
    minutes_ago: Optional[int] = None,
    hours_ago: Optional[int] = None,
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
    aggregation: str = "avg",
    anomaly_stddev_threshold: float = 2.0,
    filter_tags: Optional[Dict[str, str]] = None,
) -> MetricTrendSummary:
    """
    Summarize recent metric trends or anomalies using Datadog metrics data.

    Analyzes the queried metric series to determine:
    - Overall trend (increasing, decreasing, stable, volatile)
    - Anomalies detected using standard deviation threshold
    - Average and latest values

    Args:
        metric_name: The Datadog metric name.
        minutes_ago: How many minutes back to analyze.
        hours_ago: How many hours back to analyze.
        start_ts: Explicit start timestamp (epoch seconds).
        end_ts: Explicit end timestamp (epoch seconds).
        aggregation: Datadog aggregation function.
        anomaly_stddev_threshold: Number of standard deviations for anomaly detection.
        filter_tags: Optional tag filters.

    Returns:
        MetricTrendSummary with trend analysis and anomaly details.
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
        filter_tags=filter_tags,
    )

    config = Configuration()
    config.api_key["apiKeyAuth"] = __import__("os").environ.get("DATADOG_API_KEY", "")
    config.api_key["appKeyAuth"] = __import__("os").environ.get("DATADOG_APP_KEY", "")
    config.host = __import__("os").environ.get("DATADOG_HOST", "https://api.datadoghq.com")

    api_client = ApiClient(configuration=config)
    metrics_api = MetricsApi(api_client)

    raw_response = metrics_api.query_metrics(
        _from=from_ts,
        to=to_ts,
        query=query_string,
    )

    parsed = parse_datadog_response_to_model(raw_response)

    all_points: List[MetricDataPoint] = []
    for series in parsed.series:
        all_points.extend(series.points)

    all_points.sort(key=lambda p: p.timestamp)
    values = [p.value for p in all_points]

    if not values:
        return MetricTrendSummary(
            metric_name=metric_name,
            overall_trend="no_data",
            anomaly_count=0,
            start_ts=from_ts,
            end_ts=to_ts,
        )

    avg_val = sum(values) / len(values)
    latest_val = values[-1]
    stddev = (sum((v - avg_val) ** 2 for v in values) / len(values)) ** 0.5

    anomaly_details = []
    anomaly_count = 0
    for pt in all_points:
        if stddev > 0 and abs(pt.value - avg_val) > anomaly_stddev_threshold * stddev:
            anomaly_count += 1
            anomaly_details.append({
                "timestamp": pt.timestamp,
                "value": pt.value,
                "deviation": abs(pt.value - avg_val) / stddev,
                "type": "high" if pt.value > avg_val else "low",
            })

    trend = _determine_trend(values, stddev, avg_val)

    return MetricTrendSummary(
        metric_name=metric_name,
        overall_trend=trend,
        anomaly_count=anomaly_count,
        anomaly_details=anomaly_details,
        avg_value=avg_val,
        latest_value=latest_val,
        start_ts=from_ts,
        end_ts=to_ts,
    )


def _determine_trend(values: List[float], stddev: float, avg: float) -> str:
    """
    Determine the overall trend from a list of values.
    """
    if len(values) < 2:
        return "stable"

    n = len(values)
    mid = n // 2
    first_half_avg = sum(values[:mid]) / mid if mid > 0 else values[0]
    second_half_avg = sum(values[mid:]) / (n - mid) if (n - mid) > 0 else values[-1]

    change_ratio = abs(second_half_avg - first_half_avg) / avg if avg != 0 else 0
    relative_stddev = stddev / avg if avg != 0 else 0

    if relative_stddev > 0.5:
        return "volatile"
    elif second_half_avg > first_half_avg * 1.05:
        return "increasing"
    elif second_half_avg < first_half_avg * 0.95:
        return "decreasing"
    else:
        return "stable"
