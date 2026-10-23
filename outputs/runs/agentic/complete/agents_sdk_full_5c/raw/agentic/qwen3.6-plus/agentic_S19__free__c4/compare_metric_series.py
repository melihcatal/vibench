"""
Compare metric values for two resources or dimension filters over the same window.

Uses AWS CloudWatch GetMetricData API with multiple metric queries to retrieve
parallel time series and compute comparative statistics.

Provider signals:
  - boto3 CloudWatch (monitoring) client
  - CloudWatch GetMetricData with multiple query IDs
  - AWS CloudWatch namespace and dimension model
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from observability_client import create_cloudwatch_client, normalize_cloudwatch_response
from observability_models import MetricComparisonResult, MetricDataPoint


def compute_correlation(series_a: List[float], series_b: List[float]) -> Optional[float]:
    """Compute Pearson correlation coefficient between two series."""
    n = min(len(series_a), len(series_b))
    if n < 2:
        return None

    a = series_a[:n]
    b = series_b[:n]

    mean_a = sum(a) / n
    mean_b = sum(b) / n

    cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n)) / n
    std_a = (sum((x - mean_a) ** 2 for x in a) / n) ** 0.5
    std_b = (sum((x - mean_b) ** 2 for x in b) / n) ** 0.5

    if std_a == 0 or std_b == 0:
        return 0.0

    return cov / (std_a * std_b)


def compare_metric_series(
    metric_name: str,
    namespace: str,
    dimensions_a: Dict[str, str],
    dimensions_b: Dict[str, str],
    start_time: datetime,
    end_time: datetime,
    period: int = 60,
    statistic: str = "Average",
    label_a: Optional[str] = None,
    label_b: Optional[str] = None,
) -> MetricComparisonResult:
    """
    Compare CloudWatch metric values for two resources over the same time window.

    Retrieves two parallel metric time series from CloudWatch using GetMetricData
    with separate query entries for each dimension set.

    Args:
        metric_name: CloudWatch metric name
        namespace: CloudWatch namespace
        dimensions_a: Dimension filters for series A (e.g., {'InstanceId': 'i-abc123'})
        dimensions_b: Dimension filters for series B (e.g., {'InstanceId': 'i-def456'})
        start_time: Start of comparison window
        end_time: End of comparison window
        period: Data granularity in seconds
        statistic: CloudWatch statistic
        label_a: Human-readable label for series A
        label_b: Human-readable label for series B

    Returns:
        MetricComparisonResult with both series, deltas, and correlation.
    """
    client = create_cloudwatch_client()

    series_a_label = label_a or f"aws-resource-a"
    series_b_label = label_b or f"aws-resource-b"

    dims_a = [{"Name": k, "Value": v} for k, v in dimensions_a.items()]
    dims_b = [{"Name": k, "Value": v} for k, v in dimensions_b.items()]

    metric_queries = [
        {
            "Id": "aws-cw-series-a",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                    "Dimensions": dims_a,
                },
                "Period": period,
                "Stat": statistic,
            },
            "Label": series_a_label,
            "ReturnData": True,
        },
        {
            "Id": "aws-cw-series-b",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                    "Dimensions": dims_b,
                },
                "Period": period,
                "Stat": statistic,
            },
            "Label": series_b_label,
            "ReturnData": True,
        },
    ]

    params = {
        "StartTime": start_time,
        "EndTime": end_time,
        "MetricDataQueries": metric_queries,
        "ScanBy": "TimestampAscending",
    }

    response = client.get_metric_data(**params)
    results = normalize_cloudwatch_response(response)

    series_a_values = []
    series_b_values = []
    all_timestamps = []

    for result in results:
        metric_id = result.get("metric_id", "")
        timestamps = result.get("timestamps", [])
        values = result.get("values", [])

        if "series-a" in metric_id:
            series_a_values = list(values)
            all_timestamps = list(timestamps)
        elif "series-b" in metric_id:
            series_b_values = list(values)

    min_len = min(len(series_a_values), len(series_b_values))
    series_a_values = series_a_values[:min_len]
    series_b_values = series_b_values[:min_len]
    all_timestamps = all_timestamps[:min_len]

    delta_values = [series_a_values[i] - series_b_values[i] for i in range(min_len)]

    correlation = compute_correlation(series_a_values, series_b_values)

    return MetricComparisonResult(
        series_a_label=series_a_label,
        series_b_label=series_b_label,
        series_a_values=series_a_values,
        series_b_values=series_b_values,
        timestamps=all_timestamps,
        delta_values=delta_values,
        correlation=correlation,
    )


def compare_metric_series_simple(
    metric_name: str,
    namespace: str,
    instance_a_id: str,
    instance_b_id: str,
    duration_minutes: int = 60,
) -> MetricComparisonResult:
    """
    Simple wrapper for comparing two EC2 instances' metrics.

    Args:
        metric_name: CloudWatch metric name
        namespace: CloudWatch namespace (e.g., 'AWS/EC2')
        instance_a_id: EC2 instance ID for series A
        instance_b_id: EC2 instance ID for series B
        duration_minutes: Comparison window in minutes

    Returns:
        MetricComparisonResult.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)

    return compare_metric_series(
        metric_name=metric_name,
        namespace=namespace,
        dimensions_a={"InstanceId": instance_a_id},
        dimensions_b={"InstanceId": instance_b_id},
        start_time=start_time,
        end_time=end_time,
        label_a=f"EC2-{instance_a_id}",
        label_b=f"EC2-{instance_b_id}",
    )
