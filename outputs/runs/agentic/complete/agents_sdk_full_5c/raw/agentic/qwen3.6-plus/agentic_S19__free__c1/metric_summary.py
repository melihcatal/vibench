"""
Summarize recent metric trends or anomalies using AWS CloudWatch Anomaly Detection.

Retrieves metric data and uses CloudWatch anomaly detection bands to identify
trends, anomalies, and summarize recent metric behavior patterns.
"""

import os
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any, Tuple

from observability_client import get_cloudwatch_client, build_metric_dimensions, validate_metric_name
from observability_models import (
    MetricDataPoint,
    MetricSeries,
    MetricNamespace,
)


# CloudWatch Anomaly Detection model identifiers
CLOUDWATCH_ANOMALY_MODEL_PREFIX = "aws/cloudwatch/anomaly-detection"


class AnomalyResult:
    """Represents a single detected anomaly point."""
    def __init__(self, timestamp: datetime, actual_value: float,
                 upper_bound: float, lower_bound: float, severity: str):
        self.timestamp = timestamp
        self.actual_value = actual_value
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.severity = severity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "actual_value": self.actual_value,
            "upper_bound": self.upper_bound,
            "lower_bound": self.lower_bound,
            "severity": self.severity,
        }


class MetricTrendSummary:
    """Summary of metric trends and anomalies."""
    def __init__(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        trend: str,
        anomaly_count: int,
        anomalies: List[AnomalyResult],
        mean: float,
        std_dev: float,
        min_value: float,
        max_value: float,
        summary_text: str,
    ):
        self.metric_name = metric_name
        self.namespace = namespace
        self.start_time = start_time
        self.end_time = end_time
        self.trend = trend  # 'increasing', 'decreasing', 'stable', 'volatile'
        self.anomaly_count = anomaly_count
        self.anomalies = anomalies
        self.mean = mean
        self.std_dev = std_dev
        self.min_value = min_value
        self.max_value = max_value
        self.summary_text = summary_text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "window": {
                "start": self.start_time.isoformat(),
                "end": self.end_time.isoformat(),
            },
            "trend": self.trend,
            "anomaly_count": self.anomaly_count,
            "anomalies": [a.to_dict() for a in self.anomalies],
            "statistics": {
                "mean": self.mean,
                "std_dev": self.std_dev,
                "min": self.min_value,
                "max": self.max_value,
            },
            "summary": self.summary_text,
        }


def metric_summary(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    dimensions: Optional[Dict[str, str]] = None,
    anomaly_detection_band: int = 2,
    region: Optional[str] = None,
    client=None,
) -> MetricTrendSummary:
    """
    Summarize recent metric trends and detect anomalies using AWS CloudWatch.

    Uses CloudWatch GetMetricData with anomaly detection bands to identify
    unusual metric behavior. The anomaly detection model ID format follows
    the pattern: ad({metric_name},{namespace},{dimensions}).

    Args:
        metric_name: The CloudWatch metric name.
        namespace: The CloudWatch namespace.
        start_time: Start of the analysis window.
        end_time: End of the analysis window.
        period: Data point period in seconds.
        dimensions: Optional CloudWatch dimension filters.
        anomaly_detection_band: Number of standard deviations for anomaly band (default 2).
        region: AWS region.
        client: Optional pre-configured CloudWatch boto3 client.

    Returns:
        MetricTrendSummary with trend analysis and anomaly details.
    """
    validate_metric_name(metric_name)

    if client is None:
        client = get_cloudwatch_client(region=region)

    cw_dimensions = build_metric_dimensions(dimensions) if dimensions else []

    # Build the anomaly detection model ID for CloudWatch
    # Format: ad({metric_name},{namespace},...)
    ad_model_id = _build_anomaly_detection_model_id(
        metric_name, namespace, dimensions or {}
    )

    # Query both actual values and anomaly detection bands
    metric_data_queries = [
        {
            "Id": "actual_values",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                    "Dimensions": cw_dimensions,
                },
                "Period": period,
                "Stat": "Average",
            },
        },
        {
            "Id": "anomaly_band",
            "Expression": f"ANOMALY_DETECTION_BAND(actual_values, {anomaly_detection_band})",
        },
    ]

    params = {
        "MetricDataQueries": metric_data_queries,
        "StartTime": start_time,
        "EndTime": end_time,
    }

    response = client.get_metric_data(**params)

    # Extract actual values and anomaly bounds
    actual_values = []
    anomaly_timestamps = []
    upper_bounds = []
    lower_bounds = []

    for result in response.get("MetricDataResults", []):
        result_id = result.get("Id")
        timestamps = result.get("Timestamps", [])
        values = result.get("Values", [])

        paired = sorted(zip(timestamps, values), key=lambda x: x[0])
        ts_list = [p[0] for p in paired]
        val_list = [p[1] for p in paired]

        if result_id == "actual_values":
            actual_values = val_list
            anomaly_timestamps = ts_list
        elif result_id == "anomaly_band":
            # Anomaly band returns two values per timestamp: [lower, upper]
            upper_bounds = val_list
            lower_bounds = val_list

    # Detect anomalies where actual values fall outside the band
    anomalies = []
    if len(actual_values) > 0:
        for i, (ts, actual) in enumerate(zip(anomaly_timestamps, actual_values)):
            if i < len(upper_bounds) and i < len(lower_bounds):
                upper = upper_bounds[i]
                lower = lower_bounds[i]
                if actual > upper or actual < lower:
                    severity = _classify_severity(actual, lower, upper)
                    anomalies.append(AnomalyResult(
                        timestamp=ts,
                        actual_value=actual,
                        upper_bound=upper,
                        lower_bound=lower,
                        severity=severity,
                    ))

    # Compute trend from actual values
    trend = _compute_trend(actual_values)

    # Compute basic statistics
    values_for_stats = actual_values if actual_values else [0.0]
    mean_val = sum(values_for_stats) / len(values_for_stats)
    std_dev = _compute_std_dev(values_for_stats, mean_val)
    min_val = min(values_for_stats)
    max_val = max(values_for_stats)

    # Build summary text
    summary_text = _build_summary_text(
        metric_name, namespace, trend, len(anomalies),
        mean_val, std_dev, min_val, max_val,
    )

    return MetricTrendSummary(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        trend=trend,
        anomaly_count=len(anomalies),
        anomalies=anomalies,
        mean=mean_val,
        std_dev=std_dev,
        min_value=min_val,
        max_value=max_val,
        summary_text=summary_text,
    )


def _build_anomaly_detection_model_id(
    metric_name: str,
    namespace: str,
    dimensions: Dict[str, str],
) -> str:
    """
    Build a CloudWatch anomaly detection model identifier.

    Model ID format follows AWS CloudWatch convention:
    ad({metric_name},{namespace},{dim1_value},{dim2_value},...)

    Args:
        metric_name: CloudWatch metric name.
        namespace: CloudWatch namespace.
        dimensions: Dimension key-value pairs.

    Returns:
        CloudWatch anomaly detection model ID string.
    """
    parts = [metric_name, namespace]
    for dim_name in sorted(dimensions.keys()):
        parts.append(dimensions[dim_name])
    return f"ad({','.join(parts)})"


def _classify_severity(actual: float, lower: float, upper: float) -> str:
    """Classify anomaly severity based on how far outside the band the value is."""
    band_width = upper - lower
    if band_width == 0:
        return "moderate"

    deviation = 0
    if actual > upper:
        deviation = (actual - upper) / band_width
    elif actual < lower:
        deviation = (lower - actual) / band_width

    if deviation > 2.0:
        return "critical"
    elif deviation > 1.0:
        return "high"
    elif deviation > 0.5:
        return "moderate"
    else:
        return "low"


def _compute_trend(values: List[float]) -> str:
    """
    Compute the trend direction from a time series.

    Args:
        values: Time series values in chronological order.

    Returns:
        Trend label: 'increasing', 'decreasing', 'stable', or 'volatile'.
    """
    if len(values) < 3:
        return "stable"

    mean_val = sum(values) / len(values)
    if mean_val == 0:
        return "stable"

    # Split into first and second halves
    mid = len(values) // 2
    first_half = values[:mid]
    second_half = values[mid:]

    avg_first = sum(first_half) / len(first_half)
    avg_second = sum(second_half) / len(second_half)

    change_pct = (avg_second - avg_first) / abs(avg_first) if avg_first != 0 else 0

    # Check volatility
    std_dev = _compute_std_dev(values, mean_val)
    cv = std_dev / abs(mean_val) if mean_val != 0 else 0

    if cv > 0.5:
        return "volatile"

    if change_pct > 0.1:
        return "increasing"
    elif change_pct < -0.1:
        return "decreasing"
    else:
        return "stable"


def _compute_std_dev(values: List[float], mean: float) -> float:
    """Compute standard deviation of values."""
    if len(values) < 2:
        return 0.0
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return variance ** 0.5


def _build_summary_text(
    metric_name: str,
    namespace: str,
    trend: str,
    anomaly_count: int,
    mean: float,
    std_dev: float,
    min_val: float,
    max_val: float,
) -> str:
    """Build human-readable summary of metric analysis."""
    lines = [
        f"Metric: {metric_name} ({namespace})",
        f"Trend: {trend}",
        f"Mean: {mean:.2f} (std dev: {std_dev:.2f})",
        f"Range: [{min_val:.2f}, {max_val:.2f}]",
        f"Anomalies detected: {anomaly_count}",
    ]
    if anomaly_count > 0:
        lines.append(f"  -> {anomaly_count} data points fell outside CloudWatch anomaly detection bands")
    return "\n".join(lines)


def summarize_ec2_cpu_recent(
    instance_id: str,
    minutes_back: int = 60,
    period: int = 300,
    region: Optional[str] = None,
    client=None,
) -> MetricTrendSummary:
    """
    Summarize recent EC2 CPU utilization trends and anomalies.

    Convenience wrapper for EC2 CPU metrics.

    Args:
        instance_id: EC2 instance ID.
        minutes_back: Minutes of history.
        period: Data point period.
        region: AWS region.
        client: Optional CloudWatch client.

    Returns:
        MetricTrendSummary for the instance CPU.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)

    return metric_summary(
        metric_name="CPUUtilization",
        namespace=MetricNamespace.EC2.value,
        start_time=start_time,
        end_time=end_time,
        period=period,
        dimensions={"InstanceId": instance_id},
        region=region,
        client=client,
    )
