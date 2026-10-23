"""
Summarize recent metric trends or anomalies.

Uses AWS CloudWatch Anomaly Detection (GetMetricData with AnomalyDetection)
and CloudWatch metrics to summarize trends.

Provider signals:
  - boto3 CloudWatch (monitoring) client
  - AWS CloudWatch anomaly detection (AnomalyDetectionBandWidth)
  - CloudWatch metric math expression for anomaly detection
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from observability_client import create_cloudwatch_client, normalize_cloudwatch_response
from observability_models import MetricDataPoint


class TrendSummary:
    """Summary of metric trends and detected anomalies."""

    def __init__(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        current_value: float = 0.0,
        trend_direction: str = "stable",
        anomaly_count: int = 0,
        anomaly_timestamps: Optional[List[datetime]] = None,
        mean_value: float = 0.0,
        std_deviation: float = 0.0,
        max_value: float = 0.0,
        min_value: float = 0.0,
        upper_band: Optional[float] = None,
        lower_band: Optional[float] = None,
    ):
        self.metric_name = metric_name
        self.namespace = namespace
        self.start_time = start_time
        self.end_time = end_time
        self.current_value = current_value
        self.trend_direction = trend_direction
        self.anomaly_count = anomaly_count
        self.anomaly_timestamps = anomaly_timestamps or []
        self.mean_value = mean_value
        self.std_deviation = std_deviation
        self.max_value = max_value
        self.min_value = min_value
        self.upper_band = upper_band
        self.lower_band = lower_band

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "current_value": self.current_value,
            "trend_direction": self.trend_direction,
            "anomaly_count": self.anomaly_count,
            "anomaly_timestamps": [t.isoformat() for t in self.anomaly_timestamps],
            "mean_value": self.mean_value,
            "std_deviation": self.std_deviation,
            "max_value": self.max_value,
            "min_value": self.min_value,
            "upper_band": self.upper_band,
            "lower_band": self.lower_band,
        }


def metric_summary(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    statistic: str = "Average",
    dimensions: Optional[Dict[str, str]] = None,
    anomaly_band_width: float = 2.0,
) -> TrendSummary:
    """
    Summarize recent CloudWatch metric trends and detect anomalies.

    Uses AWS CloudWatch anomaly detection with GetMetricData and metric math
    expressions to identify trend direction and anomalies.

    Args:
        metric_name: CloudWatch metric name
        namespace: CloudWatch namespace
        start_time: Start of analysis window
        end_time: End of analysis window
        period: Data granularity in seconds
        statistic: CloudWatch statistic
        dimensions: Optional dimension filters
        anomaly_band_width: Standard deviations for anomaly band (CloudWatch default: 2.0)

    Returns:
        TrendSummary with trend analysis and anomaly information.
    """
    client = create_cloudwatch_client()

    metric_stat_entry = {
        "Id": "aws-cw-m1",
        "MetricStat": {
            "Metric": {
                "Namespace": namespace,
                "MetricName": metric_name,
            },
            "Period": period,
            "Stat": statistic,
        },
        "ReturnData": True,
    }

    if dimensions:
        dims = [{"Name": k, "Value": v} for k, v in dimensions.items()]
        metric_stat_entry["MetricStat"]["Metric"]["Dimensions"] = dims

    anomaly_query = {
        "Id": "aws-cw-anomaly",
        "Expression": f"ANOMALY_DETECTION_BAND([aws-cw-m1], {anomaly_band_width})",
        "Label": "AnomalyDetectionBand",
        "ReturnData": True,
    }

    metric_queries = [metric_stat_entry, anomaly_query]

    params = {
        "StartTime": start_time,
        "EndTime": end_time,
        "MetricDataQueries": metric_queries,
        "ScanBy": "TimestampAscending",
    }

    response = client.get_metric_data(**params)
    results = normalize_cloudwatch_response(response)

    metric_values = []
    metric_timestamps = []
    anomaly_upper = []
    anomaly_lower = []
    anomaly_timestamps = []

    for result in results:
        metric_id = result.get("metric_id", "")
        timestamps = result.get("timestamps", [])
        values = result.get("values", [])

        if "m1" in metric_id:
            metric_values = list(values)
            metric_timestamps = list(timestamps)
        elif "anomaly" in metric_id.lower():
            for ts, val in zip(timestamps, values):
                if val is not None:
                    anomaly_upper.append(val)
                    anomaly_lower.append(val)

    if not metric_values:
        return TrendSummary(
            metric_name=metric_name,
            namespace=namespace,
            start_time=start_time,
            end_time=end_time,
        )

    mean_val = sum(metric_values) / len(metric_values)
    max_val = max(metric_values)
    min_val = min(metric_values)
    current_val = metric_values[-1] if metric_values else 0.0

    std_dev = 0.0
    if len(metric_values) > 1:
        variance = sum((v - mean_val) ** 2 for v in metric_values) / len(metric_values)
        std_dev = variance ** 0.5

    n = len(metric_values)
    if n >= 3:
        first_third = sum(metric_values[: n // 3]) / (n // 3)
        last_third = sum(metric_values[-(n // 3) :]) / (n // 3)
        change_pct = (last_third - first_third) / first_third if first_third != 0 else 0.0
        if change_pct > 0.15:
            trend_direction = "increasing"
        elif change_pct < -0.15:
            trend_direction = "decreasing"
        else:
            trend_direction = "stable"
    else:
        trend_direction = "stable"

    anomaly_count = 0
    detected_anomaly_times = []
    for ts, val in zip(metric_timestamps, metric_values):
        if anomaly_upper and anomaly_lower:
            upper = max(anomaly_upper) if anomaly_upper else float("inf")
            lower = min(anomaly_lower) if anomaly_lower else float("-inf")
            if val > upper or val < lower:
                anomaly_count += 1
                detected_anomaly_times.append(ts)

    upper_band = max(anomaly_upper) if anomaly_upper else None
    lower_band = min(anomaly_lower) if anomaly_lower else None

    return TrendSummary(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        current_value=current_val,
        trend_direction=trend_direction,
        anomaly_count=anomaly_count,
        anomaly_timestamps=detected_anomaly_times,
        mean_value=mean_val,
        std_deviation=std_dev,
        max_value=max_val,
        min_value=min_val,
        upper_band=upper_band,
        lower_band=lower_band,
    )


def metric_summary_simple(
    metric_name: str,
    namespace: str,
    duration_minutes: int = 60,
) -> TrendSummary:
    """Simple wrapper summarizing the last N minutes of metric data."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)
    return metric_summary(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
    )
