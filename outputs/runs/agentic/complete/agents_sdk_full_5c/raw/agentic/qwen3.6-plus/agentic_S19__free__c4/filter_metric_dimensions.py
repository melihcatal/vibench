"""
Query metric data filtered by resource labels or dimensions.

Uses AWS CloudWatch ListMetrics and GetMetricData APIs with dimension-based
filtering for resource-scoped metric queries.

Provider signals:
  - boto3 CloudWatch (monitoring) client
  - AWS CloudWatch dimension filtering (Dimensions.Name, Dimensions.Value)
  - CloudWatch ListMetrics with dimension filters
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from observability_client import create_cloudwatch_client, normalize_cloudwatch_response
from observability_models import CloudWatchMetricQuery, MetricDataPoint


def filter_metric_dimensions(
    metric_name: str,
    namespace: str,
    dimension_filters: Dict[str, str],
    start_time: datetime,
    end_time: datetime,
    period: int = 60,
    statistic: str = "Average",
    unit: Optional[str] = None,
) -> List[MetricDataPoint]:
    """
    Query CloudWatch metric data filtered by resource dimensions/labels.

    Uses CloudWatch dimension filtering to scope metric queries to specific
    resources (e.g., specific EC2 instances, RDS databases, Lambda functions).

    Args:
        metric_name: CloudWatch metric name
        namespace: CloudWatch namespace (e.g., 'AWS/EC2', 'AWS/RDS')
        dimension_filters: Dict of dimension name to value (e.g., {'InstanceId': 'i-abc123'})
        start_time: Start of query window
        end_time: End of query window
        period: Data granularity in seconds
        statistic: CloudWatch statistic to retrieve
        unit: Optional metric unit filter

    Returns:
        List of MetricDataPoint objects matching the dimension filters.
    """
    client = create_cloudwatch_client()

    metric_queries = []
    for idx, (dim_key, dim_value) in enumerate(dimension_filters.items()):
        query_id = f"aws-cw-filter-{idx}-{dim_key}"
        query_entry = {
            "Id": query_id,
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                    "Dimensions": [
                        {"Name": dim_key, "Value": dim_value},
                    ],
                },
                "Period": period,
                "Stat": statistic,
            },
            "ReturnData": True,
        }
        if unit:
            query_entry["MetricStat"]["Metric"]["Unit"] = unit
        metric_queries.append(query_entry)

    params = {
        "StartTime": start_time,
        "EndTime": end_time,
        "MetricDataQueries": metric_queries,
        "ScanBy": "TimestampAscending",
    }

    response = client.get_metric_data(**params)
    results = normalize_cloudwatch_response(response)

    all_datapoints = []
    for result in results:
        timestamps = result.get("timestamps", [])
        values = result.get("values", [])
        label = result.get("label", "")
        for ts, val in zip(timestamps, values):
            dp = MetricDataPoint(
                timestamp=ts,
                value=val,
                unit=unit or "None",
            )
            dp._label = label
            dp._metric_id = result.get("metric_id", "")
            all_datapoints.append(dp)

    return sorted(all_datapoints, key=lambda p: p.timestamp)


def list_available_dimensions(
    metric_name: str,
    namespace: str,
) -> List[Dict[str, Any]]:
    """
    List available dimensions for a CloudWatch metric using ListMetrics API.

    Args:
        metric_name: CloudWatch metric name
        namespace: CloudWatch namespace

    Returns:
        List of metric metadata with their dimensions.
    """
    client = create_cloudwatch_client()

    params = {
        "Namespace": namespace,
        "MetricName": metric_name,
    }

    response = client.list_metrics(**params)
    metrics = response.get("Metrics", [])

    available_dimensions = []
    for metric in metrics:
        dims = {}
        for dim in metric.get("Dimensions", []):
            dims[dim["Name"]] = dim["Value"]
        if dims:
            available_dimensions.append({
                "metric_name": metric.get("MetricName"),
                "namespace": metric.get("Namespace"),
                "dimensions": dims,
            })

    return available_dimensions


def filter_metric_dimensions_multi(
    metric_name: str,
    namespace: str,
    filter_sets: List[Dict[str, str]],
    start_time: datetime,
    end_time: datetime,
    period: int = 60,
    statistic: str = "Average",
) -> Dict[str, List[MetricDataPoint]]:
    """
    Query metric data for multiple dimension filter sets in parallel.

    Each filter set is queried as a separate CloudWatch metric query entry.

    Args:
        metric_name: CloudWatch metric name
        namespace: CloudWatch namespace
        filter_sets: List of dimension filter dicts
        start_time: Start of query window
        end_time: End of query window
        period: Data granularity in seconds
        statistic: CloudWatch statistic

    Returns:
        Dict mapping filter set index string to list of MetricDataPoints.
    """
    client = create_cloudwatch_client()

    metric_queries = []
    for idx, dim_filters in enumerate(filter_sets):
        dims = [{"Name": k, "Value": v} for k, v in dim_filters.items()]
        query_id = f"aws-cw-multi-{idx}"
        query_entry = {
            "Id": query_id,
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                    "Dimensions": dims,
                },
                "Period": period,
                "Stat": statistic,
            },
            "ReturnData": True,
        }
        metric_queries.append(query_entry)

    params = {
        "StartTime": start_time,
        "EndTime": end_time,
        "MetricDataQueries": metric_queries,
    }

    response = client.get_metric_data(**params)
    results = normalize_cloudwatch_response(response)

    output = {}
    for result in results:
        metric_id = result.get("metric_id", "")
        timestamps = result.get("timestamps", [])
        values = result.get("values", [])
        dps = []
        for ts, val in zip(timestamps, values):
            dps.append(MetricDataPoint(timestamp=ts, value=val, unit="None"))
        output[metric_id] = sorted(dps, key=lambda p: p.timestamp)

    return output
