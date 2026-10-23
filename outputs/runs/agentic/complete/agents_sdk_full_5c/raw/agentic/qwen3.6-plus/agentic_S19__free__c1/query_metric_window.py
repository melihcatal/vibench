"""
Query recent datapoints for a named metric over a time window using AWS CloudWatch.

Retrieves raw time-series data points for a specific metric within a defined
start/end time window. Uses the AWS CloudWatch GetMetricData API via boto3.
"""

import os
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any

from observability_client import get_cloudwatch_client, build_metric_dimensions, validate_metric_name
from observability_models import (
    MetricQueryRequest,
    MetricDataPoint,
    MetricSeries,
    MetricNamespace,
)


def query_metric_window(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    dimensions: Optional[Dict[str, str]] = None,
    statistics: Optional[List[str]] = None,
    unit: Optional[str] = None,
    region: Optional[str] = None,
    client=None,
) -> MetricSeries:
    """
    Query recent datapoints for a named metric over a time window from AWS CloudWatch.

    Uses the CloudWatch GetMetricData API (endpoint: monitoring.amazonaws.com)
    to retrieve time-series data points.

    Args:
        metric_name: The CloudWatch metric name (e.g., 'CPUUtilization').
        namespace: The CloudWatch namespace (e.g., 'AWS/EC2').
        start_time: Start of the query window (timezone-aware datetime).
        end_time: End of the query window (timezone-aware datetime).
        period: Data point period in seconds (default 300 = 5 min).
        dimensions: Optional dict of CloudWatch dimension filters.
        statistics: List of stats to retrieve (default ['Average']).
        unit: Optional CloudWatch unit filter (e.g., 'Percent', 'Bytes').
        region: AWS region for the CloudWatch endpoint.
        client: Optional pre-configured CloudWatch boto3 client.

    Returns:
        MetricSeries containing the queried datapoints.

    Raises:
        ValueError: If metric_name is invalid or times are out of range.
    """
    validate_metric_name(metric_name)

    if start_time >= end_time:
        raise ValueError("start_time must be before end_time")

    if client is None:
        client = get_cloudwatch_client(region=region)

    cw_dimensions = build_metric_dimensions(dimensions) if dimensions else None
    stats = statistics or ["Average"]

    request = MetricQueryRequest(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period,
        dimensions=cw_dimensions,
        statistics=stats,
        unit=unit,
    )

    params = request.to_cloudwatch_params()

    response = client.get_metric_data(**params)

    datapoints = []
    unit_value = unit or "Count"

    for metric_result in response.get("MetricDataResults", []):
        for i, ts in enumerate(metric_result.get("Timestamps", [])):
            values = metric_result.get("Values", [])
            if i < len(values):
                datapoints.append(MetricDataPoint(
                    timestamp=ts,
                    value=float(values[i]),
                    unit=unit_value,
                ))

    datapoints.sort(key=lambda dp: dp.timestamp)

    result_dimensions = cw_dimensions or []
    return MetricSeries(
        metric_name=metric_name,
        namespace=namespace,
        dimensions=result_dimensions,
        datapoints=datapoints,
        statistics=stats,
    )


def query_metric_window_recent(
    metric_name: str,
    namespace: str,
    minutes_back: int = 60,
    period: int = 300,
    dimensions: Optional[Dict[str, str]] = None,
    statistics: Optional[List[str]] = None,
    region: Optional[str] = None,
    client=None,
) -> MetricSeries:
    """
    Convenience function to query a metric for the last N minutes.

    Args:
        metric_name: The CloudWatch metric name.
        namespace: The CloudWatch namespace.
        minutes_back: Number of minutes to look back (default 60).
        period: Data point period in seconds.
        dimensions: Optional dimension filters.
        statistics: Statistics to retrieve.
        region: AWS region.
        client: Optional pre-configured CloudWatch boto3 client.

    Returns:
        MetricSeries with recent datapoints.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)

    return query_metric_window(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period,
        dimensions=dimensions,
        statistics=statistics,
        region=region,
        client=client,
    )


def query_ec2_cpu_utilization(
    instance_id: str,
    minutes_back: int = 60,
    region: Optional[str] = None,
    client=None,
) -> MetricSeries:
    """
    Query EC2 CPUUtilization metric for a specific instance.

    Convenience wrapper targeting AWS/EC2 namespace with CPUUtilization metric.

    Args:
        instance_id: EC2 instance ID (e.g., 'i-0abc123def456').
        minutes_back: Minutes of history to retrieve.
        region: AWS region.
        client: Optional pre-configured CloudWatch client.

    Returns:
        MetricSeries with CPU utilization datapoints.
    """
    return query_metric_window_recent(
        metric_name="CPUUtilization",
        namespace=MetricNamespace.EC2.value,
        minutes_back=minutes_back,
        dimensions={"InstanceId": instance_id},
        statistics=["Average", "Maximum"],
        region=region,
        client=client,
    )
