"""
Compare metric values for two resources or dimension filters over the same window
using AWS CloudWatch.

Retrieves parallel time-series data for two different resources or dimension sets
and computes comparative statistics, correlations, and percent differences.
"""

import os
import math
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any, Tuple

from observability_client import get_cloudwatch_client, build_metric_dimensions, validate_metric_name
from observability_models import (
    MetricDataPoint,
    MetricSeries,
    MetricComparisonResult,
    MetricNamespace,
)


def compare_metric_series(
    metric_name: str,
    namespace: str,
    dimensions_a: Dict[str, str],
    dimensions_b: Dict[str, str],
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    statistics: Optional[List[str]] = None,
    unit: Optional[str] = None,
    region: Optional[str] = None,
    client=None,
) -> MetricComparisonResult:
    """
    Compare metric values for two resources or dimension filters over the same window.

    Queries AWS CloudWatch GetMetricData API (monitoring.amazonaws.com) for both
    dimension sets in parallel and computes comparative statistics.

    Args:
        metric_name: The CloudWatch metric name.
        namespace: The CloudWatch namespace.
        dimensions_a: First resource's dimension filters.
        dimensions_b: Second resource's dimension filters.
        start_time: Start of comparison window.
        end_time: End of comparison window.
        period: Data point period in seconds.
        statistics: List of stats to retrieve (default ['Average']).
        unit: Optional CloudWatch unit filter.
        region: AWS region.
        client: Optional pre-configured CloudWatch boto3 client.

    Returns:
        MetricComparisonResult with parallel data and comparative analysis.
    """
    validate_metric_name(metric_name)

    if start_time >= end_time:
        raise ValueError("start_time must be before end_time")

    if client is None:
        client = get_cloudwatch_client(region=region)

    stats = statistics or ["Average"]

    # Query both dimension sets via CloudWatch GetMetricData
    params = {
        "MetricDataQueries": [
            {
                "Id": "series_a",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": build_metric_dimensions(dimensions_a),
                    },
                    "Period": period,
                    "Stat": stats[0],
                },
            },
            {
                "Id": "series_b",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": build_metric_dimensions(dimensions_b),
                    },
                    "Period": period,
                    "Stat": stats[0],
                },
            },
        ],
        "StartTime": start_time,
        "EndTime": end_time,
    }

    if unit:
        params["MetricDataQueries"][0]["MetricStat"]["Unit"] = unit
        params["MetricDataQueries"][1]["MetricStat"]["Unit"] = unit

    response = client.get_metric_data(**params)

    series_a = _extract_series_from_response(response, "series_a", metric_name, namespace, dimensions_a, stats)
    series_b = _extract_series_from_response(response, "series_b", metric_name, namespace, dimensions_b, stats)

    # Compute comparison metrics
    correlation = _compute_correlation(series_a.values, series_b.values)
    avg_a = sum(series_a.values) / len(series_a.values) if series_a.values else 0.0
    avg_b = sum(series_b.values) / len(series_b.values) if series_b.values else 0.0
    percent_diff = _compute_percent_difference(avg_a, avg_b)

    summary = _build_comparison_summary(
        metric_name, namespace, avg_a, avg_b, correlation, percent_diff,
        dimensions_a, dimensions_b,
    )

    return MetricComparisonResult(
        series_a=series_a,
        series_b=series_b,
        correlation=correlation,
        percent_difference=percent_diff,
        summary=summary,
    )


def compare_ec2_instances(
    metric_name: str,
    instance_id_a: str,
    instance_id_b: str,
    minutes_back: int = 60,
    period: int = 300,
    statistics: Optional[List[str]] = None,
    region: Optional[str] = None,
    client=None,
) -> MetricComparisonResult:
    """
    Compare a metric between two EC2 instances.

    Convenience wrapper targeting AWS/EC2 namespace for instance comparison.

    Args:
        metric_name: Metric to compare (e.g., 'CPUUtilization', 'NetworkIn').
        instance_id_a: First EC2 instance ID.
        instance_id_b: Second EC2 instance ID.
        minutes_back: Minutes of history.
        period: Data point period in seconds.
        statistics: Statistics to retrieve.
        region: AWS region.
        client: Optional CloudWatch client.

    Returns:
        MetricComparisonResult for the two instances.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)

    return compare_metric_series(
        metric_name=metric_name,
        namespace=MetricNamespace.EC2.value,
        dimensions_a={"InstanceId": instance_id_a},
        dimensions_b={"InstanceId": instance_id_b},
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=statistics,
        region=region,
        client=client,
    )


def compare_rds_instances(
    metric_name: str,
    db_instance_a: str,
    db_instance_b: str,
    minutes_back: int = 60,
    period: int = 300,
    region: Optional[str] = None,
    client=None,
) -> MetricComparisonResult:
    """
    Compare a metric between two RDS database instances.

    Convenience wrapper targeting AWS/RDS namespace.

    Args:
        metric_name: Metric to compare (e.g., 'CPUUtilization', 'DatabaseConnections').
        db_instance_a: First RDS instance identifier.
        db_instance_b: Second RDS instance identifier.
        minutes_back: Minutes of history.
        period: Data point period in seconds.
        region: AWS region.
        client: Optional CloudWatch client.

    Returns:
        MetricComparisonResult for the two RDS instances.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)

    return compare_metric_series(
        metric_name=metric_name,
        namespace=MetricNamespace.RDS.value,
        dimensions_a={"DBInstanceIdentifier": db_instance_a},
        dimensions_b={"DBInstanceIdentifier": db_instance_b},
        start_time=start_time,
        end_time=end_time,
        period=period,
        region=region,
        client=client,
    )


def _extract_series_from_response(
    response: Dict[str, Any],
    query_id: str,
    metric_name: str,
    namespace: str,
    dimensions: Dict[str, str],
    statistics: List[str],
) -> MetricSeries:
    """
    Extract a MetricSeries from a CloudWatch GetMetricData response.

    Args:
        response: CloudWatch GetMetricData response.
        query_id: The query ID to extract ('series_a' or 'series_b').
        metric_name: Metric name.
        namespace: CloudWatch namespace.
        dimensions: Dimension dict for this series.
        statistics: Statistics list.

    Returns:
        MetricSeries with the extracted datapoints.
    """
    datapoints = []
    cw_dimensions = build_metric_dimensions(dimensions)

    for metric_result in response.get("MetricDataResults", []):
        if metric_result.get("Id") == query_id:
            for i, ts in enumerate(metric_result.get("Timestamps", [])):
                values = metric_result.get("Values", [])
                if i < len(values):
                    datapoints.append(MetricDataPoint(
                        timestamp=ts,
                        value=float(values[i]),
                        unit="Count",
                    ))
            break

    datapoints.sort(key=lambda dp: dp.timestamp)

    return MetricSeries(
        metric_name=metric_name,
        namespace=namespace,
        dimensions=cw_dimensions,
        datapoints=datapoints,
        statistics=statistics,
    )


def _compute_correlation(values_a: List[float], values_b: List[float]) -> Optional[float]:
    """
    Compute Pearson correlation between two time series.

    Aligns series by taking the minimum length and computing correlation coefficient.

    Args:
        values_a: First series values.
        values_b: Second series values.

    Returns:
        Correlation coefficient in [-1, 1], or None if insufficient data.
    """
    n = min(len(values_a), len(values_b))
    if n < 2:
        return None

    a = values_a[:n]
    b = values_b[:n]

    mean_a = sum(a) / n
    mean_b = sum(b) / n

    numerator = sum((ai - mean_a) * (bi - mean_b) for ai, bi in zip(a, b))
    denom_a = math.sqrt(sum((ai - mean_a) ** 2 for ai in a))
    denom_b = math.sqrt(sum((bi - mean_b) ** 2 for bi in b))

    if denom_a == 0 or denom_b == 0:
        return 0.0

    return numerator / (denom_a * denom_b)


def _compute_percent_difference(avg_a: float, avg_b: float) -> Optional[float]:
    """
    Compute percent difference between two averages.

    Uses the average of the two values as the reference.

    Args:
        avg_a: First series average.
        avg_b: Second series average.

    Returns:
        Percent difference, or None if both are zero.
    """
    reference = (abs(avg_a) + abs(avg_b)) / 2
    if reference == 0:
        return None
    return ((avg_a - avg_b) / reference) * 100


def _build_comparison_summary(
    metric_name: str,
    namespace: str,
    avg_a: float,
    avg_b: float,
    correlation: Optional[float],
    percent_diff: Optional[float],
    dims_a: Dict[str, str],
    dims_b: Dict[str, str],
) -> str:
    """
    Build a human-readable summary of the comparison.

    Args:
        metric_name: Metric being compared.
        namespace: CloudWatch namespace.
        avg_a: Series A average.
        avg_b: Series B average.
        correlation: Pearson correlation.
        percent_diff: Percent difference.
        dims_a: Series A dimensions.
        dims_b: Series B dimensions.

    Returns:
        Summary string.
    """
    parts = [
        f"Comparison of {metric_name} ({namespace})",
        f"  Series A {dims_a}: avg={avg_a:.2f}",
        f"  Series B {dims_b}: avg={avg_b:.2f}",
    ]
    if percent_diff is not None:
        parts.append(f"  Percent difference: {percent_diff:.1f}%")
    if correlation is not None:
        parts.append(f"  Correlation: {correlation:.3f}")
    return "\n".join(parts)
