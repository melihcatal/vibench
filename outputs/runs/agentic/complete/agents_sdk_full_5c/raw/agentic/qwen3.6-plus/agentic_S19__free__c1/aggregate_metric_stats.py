"""
Retrieve aggregated statistics for a metric over a time window using AWS CloudWatch.

Computes aggregated statistics (min, max, avg, sum, sample count, percentiles)
for a metric using the CloudWatch GetMetricStatistics and GetMetricData APIs.
"""

import os
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any

from observability_client import get_cloudwatch_client, build_metric_dimensions, validate_metric_name
from observability_models import (
    MetricAggregationResult,
    MetricStat,
    MetricNamespace,
)


def aggregate_metric_stats(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    dimensions: Optional[Dict[str, str]] = None,
    statistics: Optional[List[str]] = None,
    extended_statistics: Optional[List[str]] = None,
    unit: Optional[str] = None,
    region: Optional[str] = None,
    client=None,
) -> MetricAggregationResult:
    """
    Retrieve aggregated statistics for a metric over a time window from AWS CloudWatch.

    Uses the CloudWatch GetMetricStatistics API (monitoring.amazonaws.com) to
    compute aggregate values across the specified time window.

    Args:
        metric_name: The CloudWatch metric name.
        namespace: The CloudWatch namespace.
        start_time: Start of the aggregation window.
        end_time: End of the aggregation window.
        period: Aggregation period in seconds (default 300).
        dimensions: Optional dict of CloudWatch dimension filters.
        statistics: Standard statistics (Average, Sum, Minimum, Maximum, SampleCount).
        extended_statistics: Percentile stats like 'p50', 'p90', 'p99'.
        unit: Optional CloudWatch unit filter.
        region: AWS region.
        client: Optional pre-configured CloudWatch boto3 client.

    Returns:
        MetricAggregationResult with computed aggregate values.
    """
    validate_metric_name(metric_name)

    if start_time >= end_time:
        raise ValueError("start_time must be before end_time")

    if client is None:
        client = get_cloudwatch_client(region=region)

    cw_dimensions = build_metric_dimensions(dimensions) if dimensions else []

    # CloudWatch GetMetricStatistics requires at least one statistic
    stats = statistics or ["Average"]
    extended = extended_statistics or []

    params = {
        "Namespace": namespace,
        "MetricName": metric_name,
        "Dimensions": cw_dimensions,
        "StartTime": start_time,
        "EndTime": end_time,
        "Period": period,
        "Statistics": stats,
    }

    if extended:
        params["ExtendedStatistics"] = extended

    if unit:
        params["Unit"] = unit

    response = client.get_metric_statistics(**params)

    datapoints = response.get("Datapoints", [])
    aggregated = _compute_aggregates(datapoints, stats, extended)

    unit_value = _resolve_unit_from_response(datapoints, unit)

    return MetricAggregationResult(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=aggregated,
        datapoint_count=len(datapoints),
        unit=unit_value,
    )


def _compute_aggregates(
    datapoints: List[Dict[str, Any]],
    statistics: List[str],
    extended_statistics: List[str],
) -> Dict[str, float]:
    """
    Compute aggregate values across multiple CloudWatch datapoints.

    Args:
        datapoints: List of datapoints from CloudWatch response.
        statistics: List of standard statistic names to aggregate.
        extended_statistics: List of extended statistic names.

    Returns:
        Dictionary mapping aggregated statistic names to their computed values.
    """
    if not datapoints:
        return {}

    aggregates = {}

    for stat in statistics:
        values = [dp.get(stat) for dp in datapoints if dp.get(stat) is not None]
        if values:
            if stat in ("Average", "Minimum", "Maximum", "Sum"):
                aggregates[f"overall_{stat.lower()}"] = sum(values) / len(values)
                aggregates[f"min_{stat.lower()}"] = min(values)
                aggregates[f"max_{stat.lower()}"] = max(values)
            elif stat == "SampleCount":
                aggregates[f"total_{stat.lower()}"] = sum(values)
                aggregates[f"avg_{stat.lower()}"] = sum(values) / len(values)

    for ext_stat in extended_statistics:
        values = []
        for dp in datapoints:
            ext_vals = dp.get("ExtendedStatistics", {})
            if ext_stat in ext_vals:
                values.append(ext_vals[ext_stat])
        if values:
            aggregates[f"overall_{ext_stat}"] = sum(values) / len(values)
            aggregates[f"min_{ext_stat}"] = min(values)
            aggregates[f"max_{ext_stat}"] = max(values)

    return aggregates


def _resolve_unit_from_response(datapoints: List[Dict[str, Any]], default_unit: Optional[str]) -> str:
    """Resolve the unit from CloudWatch response datapoints."""
    for dp in datapoints:
        if "Unit" in dp:
            return dp["Unit"]
    return default_unit or "Count"


def aggregate_ec2_cpu_stats(
    instance_id: str,
    minutes_back: int = 60,
    period: int = 300,
    region: Optional[str] = None,
    client=None,
) -> MetricAggregationResult:
    """
    Convenience function to aggregate EC2 CPU utilization statistics.

    Args:
        instance_id: EC2 instance ID.
        minutes_back: Number of minutes to look back.
        period: Aggregation period in seconds.
        region: AWS region.
        client: Optional pre-configured CloudWatch client.

    Returns:
        MetricAggregationResult with CPU utilization aggregates.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)

    return aggregate_metric_stats(
        metric_name="CPUUtilization",
        namespace=MetricNamespace.EC2.value,
        start_time=start_time,
        end_time=end_time,
        period=period,
        dimensions={"InstanceId": instance_id},
        statistics=["Average", "Maximum", "Minimum", "SampleCount"],
        extended_statistics=["p90", "p95", "p99"],
        unit="Percent",
        region=region,
        client=client,
    )


def aggregate_lambda_duration_stats(
    function_name: str,
    minutes_back: int = 60,
    period: int = 60,
    region: Optional[str] = None,
    client=None,
) -> MetricAggregationResult:
    """
    Convenience function to aggregate Lambda Duration statistics.

    Args:
        function_name: Lambda function name.
        minutes_back: Minutes of history.
        period: Aggregation period in seconds.
        region: AWS region.
        client: Optional pre-configured CloudWatch client.

    Returns:
        MetricAggregationResult with Lambda duration aggregates.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)

    return aggregate_metric_stats(
        metric_name="Duration",
        namespace=MetricNamespace.LAMBDA.value,
        start_time=start_time,
        end_time=end_time,
        period=period,
        dimensions={"FunctionName": function_name},
        statistics=["Average", "Maximum", "Minimum", "Sum", "SampleCount"],
        extended_statistics=["p50", "p90", "p99"],
        unit="Milliseconds",
        region=region,
        client=client,
    )
