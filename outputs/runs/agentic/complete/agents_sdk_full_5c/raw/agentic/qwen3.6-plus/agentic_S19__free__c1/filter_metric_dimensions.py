"""
Query metric data filtered by resource labels or dimensions using AWS CloudWatch.

Retrieves metric data with dimension-based filtering (resource labels, instance tags,
environment labels) to scope metric queries to specific resources or groups.
"""

import os
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any, Set

from observability_client import get_cloudwatch_client, build_metric_dimensions, validate_metric_name
from observability_models import (
    MetricDataPoint,
    MetricSeries,
    MetricNamespace,
)


def filter_metric_dimensions(
    metric_name: str,
    namespace: str,
    dimension_filters: Dict[str, List[str]],
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    statistics: Optional[List[str]] = None,
    unit: Optional[str] = None,
    region: Optional[str] = None,
    client=None,
) -> List[MetricSeries]:
    """
    Query metric data filtered by resource labels/dimensions from AWS CloudWatch.

    Uses the CloudWatch ListMetrics and GetMetricData APIs to retrieve data for
    metrics that match the specified dimension filters (e.g., InstanceId,
    Environment, ServiceName labels).

    Args:
        metric_name: The CloudWatch metric name.
        namespace: The CloudWatch namespace.
        dimension_filters: Dict mapping dimension names to lists of allowed values.
            Example: {"Environment": ["prod", "staging"], "InstanceType": ["t3.large"]}
        start_time: Start of the query window.
        end_time: End of the query window.
        period: Data point period in seconds.
        statistics: List of stats to retrieve (default ['Average']).
        unit: Optional CloudWatch unit filter.
        region: AWS region for CloudWatch endpoint.
        client: Optional pre-configured CloudWatch boto3 client.

    Returns:
        List of MetricSeries, one per matching dimension combination.
    """
    validate_metric_name(metric_name)

    if start_time >= end_time:
        raise ValueError("start_time must be before end_time")

    if client is None:
        client = get_cloudwatch_client(region=region)

    # First, use ListMetrics to discover matching dimension combinations
    matching_dimensions = _list_matching_dimensions(
        client=client,
        metric_name=metric_name,
        namespace=namespace,
        dimension_filters=dimension_filters,
    )

    if not matching_dimensions:
        return []

    # Then query data for each matching dimension set
    series_list = []
    stats = statistics or ["Average"]

    for dim_set in matching_dimensions:
        cw_dimensions = build_metric_dimensions(dim_set)
        series = _query_dimension_set(
            client=client,
            metric_name=metric_name,
            namespace=namespace,
            dimensions=cw_dimensions,
            start_time=start_time,
            end_time=end_time,
            period=period,
            statistics=stats,
            unit=unit,
        )
        if series.datapoints:
            series_list.append(series)

    return series_list


def _list_matching_dimensions(
    client,
    metric_name: str,
    namespace: str,
    dimension_filters: Dict[str, List[str]],
) -> List[Dict[str, str]]:
    """
    Use CloudWatch ListMetrics API to find all dimension combinations that match
    the specified dimension filters.

    Args:
        client: CloudWatch boto3 client.
        metric_name: Metric name to search.
        namespace: CloudWatch namespace.
        dimension_filters: Dimension name -> list of allowed values.

    Returns:
        List of dimension dicts that match the filters.
    """
    matching = []

    params = {
        "Namespace": namespace,
        "MetricName": metric_name,
    }

    # If there are filters, we can try to paginate through ListMetrics
    # CloudWatch returns metrics with their dimensions
    paginator = client.get_paginator("list_metrics")
    pages = paginator.paginate(**params)

    for page in pages:
        for metric_entry in page.get("Metrics", []):
            dims = metric_entry.get("Dimensions", [])
            dim_dict = {d["Name"]: d["Value"] for d in dims}

            if _matches_filters(dim_dict, dimension_filters):
                matching.append(dim_dict)

    # Deduplicate by dimension key signature
    seen = set()
    unique = []
    for dim_dict in matching:
        sig = tuple(sorted(dim_dict.items()))
        if sig not in seen:
            seen.add(sig)
            unique.append(dim_dict)

    return unique


def _matches_filters(
    metric_dims: Dict[str, str],
    dimension_filters: Dict[str, List[str]],
) -> bool:
    """
    Check if a metric's dimensions match the provided filters.

    Args:
        metric_dims: The actual dimensions on a CloudWatch metric.
        dimension_filters: The filters to match against.

    Returns:
        True if all specified filters are satisfied.
    """
    for dim_name, allowed_values in dimension_filters.items():
        if dim_name not in metric_dims:
            return False
        if metric_dims[dim_name] not in allowed_values:
            return False
    return True


def _query_dimension_set(
    client,
    metric_name: str,
    namespace: str,
    dimensions: List[Dict[str, str]],
    start_time: datetime,
    end_time: datetime,
    period: int,
    statistics: List[str],
    unit: Optional[str],
) -> MetricSeries:
    """
    Query metric data for a single dimension set.

    Args:
        client: CloudWatch boto3 client.
        metric_name: Metric name.
        namespace: CloudWatch namespace.
        dimensions: List of dimension dicts for this series.
        start_time: Start of query window.
        end_time: End of query window.
        period: Data point period.
        statistics: Statistics to retrieve.
        unit: Optional unit filter.

    Returns:
        MetricSeries with the queried datapoints.
    """
    import hashlib

    dim_signature = hashlib.md5(
        str(sorted(str(d) for d in dimensions)).encode()
    ).hexdigest()[:8]

    params = {
        "MetricDataQueries": [
            {
                "Id": f"dim_query_{dim_signature}",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": dimensions,
                    },
                    "Period": period,
                    "Stat": statistics[0],
                },
            }
        ],
        "StartTime": start_time,
        "EndTime": end_time,
    }

    if unit:
        params["MetricDataQueries"][0]["MetricStat"]["Unit"] = unit

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

    return MetricSeries(
        metric_name=metric_name,
        namespace=namespace,
        dimensions=dimensions,
        datapoints=datapoints,
        statistics=statistics,
    )


def filter_by_environment(
    metric_name: str,
    namespace: str,
    environments: List[str],
    minutes_back: int = 60,
    period: int = 300,
    region: Optional[str] = None,
    client=None,
) -> List[MetricSeries]:
    """
    Filter metric data by Environment dimension label.

    Convenience wrapper for filtering metrics by deployment environment
    (e.g., 'prod', 'staging', 'dev') in CloudWatch.

    Args:
        metric_name: CloudWatch metric name.
        namespace: CloudWatch namespace.
        environments: List of environment labels to include.
        minutes_back: Minutes of history.
        period: Data point period.
        region: AWS region.
        client: Optional CloudWatch client.

    Returns:
        List of MetricSeries for matching environments.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)

    return filter_metric_dimensions(
        metric_name=metric_name,
        namespace=namespace,
        dimension_filters={"Environment": environments},
        start_time=start_time,
        end_time=end_time,
        period=period,
        region=region,
        client=client,
    )


def filter_by_resource_group(
    metric_name: str,
    namespace: str,
    resource_ids: List[str],
    dimension_name: str = "InstanceId",
    minutes_back: int = 60,
    period: int = 300,
    region: Optional[str] = None,
    client=None,
) -> List[MetricSeries]:
    """
    Filter metric data by a group of resource IDs.

    Convenience wrapper for filtering metrics by specific resource identifiers
    like EC2 InstanceId, RDS DBInstanceIdentifier, etc.

    Args:
        metric_name: CloudWatch metric name.
        namespace: CloudWatch namespace.
        resource_ids: List of resource identifiers.
        dimension_name: CloudWatch dimension name (default 'InstanceId').
        minutes_back: Minutes of history.
        period: Data point period.
        region: AWS region.
        client: Optional CloudWatch client.

    Returns:
        List of MetricSeries for matching resources.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)

    return filter_metric_dimensions(
        metric_name=metric_name,
        namespace=namespace,
        dimension_filters={dimension_name: resource_ids},
        start_time=start_time,
        end_time=end_time,
        period=period,
        region=region,
        client=client,
    )
