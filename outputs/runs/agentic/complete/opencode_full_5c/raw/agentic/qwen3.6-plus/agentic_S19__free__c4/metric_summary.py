import math
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from observability_client import ObservabilityClient
from observability_models import (
    MetricDataPoint,
    MetricDimension,
    MetricStatistic,
    MetricTrendSummary,
    normalize_period_to_seconds,
    parse_dimension_string,
)

CLOUDWATCH_NAMESPACE = "AWS/EC2"
DEFAULT_METRIC_NAME = "CPUUtilization"
DEFAULT_PERIOD_MINUTES = 5
ANOMALY_THRESHOLD_SIGMAS = 2.0


def metric_summary(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    dimensions: Optional[List[MetricDimension]] = None,
    statistic: MetricStatistic = MetricStatistic.AVERAGE,
    anomaly_threshold_sigmas: float = ANOMALY_THRESHOLD_SIGMAS,
    region: Optional[str] = None,
) -> MetricTrendSummary:
    period_seconds = normalize_period_to_seconds(period_minutes)

    client = ObservabilityClient(region=region)

    response = client.get_metric_data(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        dimensions=dimensions,
        statistics=[statistic],
    )

    datapoints = response.datapoints

    if not datapoints:
        return MetricTrendSummary(
            metric_name=metric_name,
            namespace=namespace,
            trend_direction="unknown",
            anomaly_count=0,
            anomalies=[],
            average_value=0.0,
            min_value=0.0,
            max_value=0.0,
            std_deviation=0.0,
        )

    values = [dp.value for dp in datapoints]
    n = len(values)

    avg = sum(values) / n
    min_val = min(values)
    max_val = max(values)

    if n > 1:
        variance = sum((v - avg) ** 2 for v in values) / (n - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0.0

    trend_direction = _detect_trend(values)

    anomalies = []
    if std_dev > 0:
        for i, dp in enumerate(datapoints):
            z_score = abs(dp.value - avg) / std_dev
            if z_score > anomaly_threshold_sigmas:
                anomalies.append(
                    {
                        "timestamp": dp.timestamp.isoformat(),
                        "value": dp.value,
                        "z_score": round(z_score, 4),
                        "deviation": round(dp.value - avg, 4),
                    }
                )

    return MetricTrendSummary(
        metric_name=metric_name,
        namespace=namespace,
        trend_direction=trend_direction,
        anomaly_count=len(anomalies),
        anomalies=anomalies,
        average_value=round(avg, 4),
        min_value=round(min_val, 4),
        max_value=round(max_val, 4),
        std_deviation=round(std_dev, 4),
    )


def metric_summary_by_string(
    namespace: str = CLOUDWATCH_NAMESPACE,
    metric_name: str = DEFAULT_METRIC_NAME,
    window_minutes: int = 60,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    dimensions_str: str = "",
    statistic: str = "Average",
    anomaly_threshold_sigmas: float = ANOMALY_THRESHOLD_SIGMAS,
    region: Optional[str] = None,
) -> MetricTrendSummary:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)

    dimensions = parse_dimension_string(dimensions_str)
    stat_enum = MetricStatistic(statistic)

    return metric_summary(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period_minutes=period_minutes,
        dimensions=dimensions,
        statistic=stat_enum,
        anomaly_threshold_sigmas=anomaly_threshold_sigmas,
        region=region,
    )


def _detect_trend(values: List[float]) -> str:
    if len(values) < 3:
        return "insufficient_data"

    n = len(values)
    first_half_avg = sum(values[: n // 2]) / (n // 2)
    second_half_avg = sum(values[n // 2 :]) / (n - n // 2)

    overall_avg = sum(values) / n
    threshold = overall_avg * 0.05

    diff = second_half_avg - first_half_avg

    if diff > threshold:
        return "increasing"
    elif diff < -threshold:
        return "decreasing"
    else:
        return "stable"


def format_summary_results(summary: MetricTrendSummary) -> str:
    lines = [
        f"Summary: {summary.namespace}/{summary.metric_name}",
        f"Trend: {summary.trend_direction}",
        f"Average: {summary.average_value:.4f}",
        f"Min: {summary.min_value:.4f}",
        f"Max: {summary.max_value:.4f}",
        f"Std Deviation: {summary.std_deviation:.4f}",
        f"Anomalies detected: {summary.anomaly_count}",
    ]

    if summary.anomalies:
        lines.append("")
        lines.append("Anomaly details:")
        for anomaly in summary.anomalies:
            lines.append(
                f"  {anomaly['timestamp']} | value={anomaly['value']:.4f} "
                f"z_score={anomaly['z_score']:.2f}"
            )

    return "\n".join(lines)
