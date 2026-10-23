"""
Query recent datapoints for a named metric over a time window.

Uses AWS CloudWatch GetMetricData API to retrieve time-series metric data.
Provider signals:
  - boto3 CloudWatch (monitoring) client
  - CloudWatch-specific query ID format (aws/cw-metric-query)
  - AWS environment variables
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from observability_client import create_cloudwatch_client, normalize_cloudwatch_response
from observability_models import (
    CloudWatchMetricQuery,
    MetricDataPoint,
    normalize_metric_datapoints,
)


def query_metric_window(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 60,
    statistic: str = "Average",
    dimensions: Optional[Dict[str, str]] = None,
    unit: Optional[str] = None,
) -> List[MetricDataPoint]:
    """
    Query CloudWatch for recent datapoints of a named metric over a time window.

    Args:
        metric_name: Name of the CloudWatch metric (e.g., 'CPUUtilization')
        namespace: CloudWatch metric namespace (e.g., 'AWS/EC2')
        start_time: Start of the query window
        end_time: End of the query window
        period: Data granularity in seconds
        statistic: CloudWatch statistic (Average, Sum, Maximum, Minimum, SampleCount)
        dimensions: Optional dimension filters (e.g., {'InstanceId': 'i-abc123'})
        unit: Optional metric unit filter

    Returns:
        List of normalized MetricDataPoint objects sorted by timestamp.
    """
    client = create_cloudwatch_client()

    query_id = f"aws-cw-{metric_name}-{int(start_time.timestamp())}"
    cw_query = CloudWatchMetricQuery(
        query_id=query_id,
        metric_name=metric_name,
        namespace=namespace,
        dimensions=dimensions,
        statistic=statistic,
        period=period,
        unit=unit,
    )

    metric_queries = [
        {
            "Id": cw_query.query_id,
            "MetricStat": {
                "Metric": {
                    "Namespace": cw_query.namespace,
                    "MetricName": cw_query.metric_name,
                },
                "Period": cw_query.period,
                "Stat": cw_query.statistic,
            },
            "ReturnData": True,
        }
    ]

    if dimensions:
        dims = [{"Name": k, "Value": v} for k, v in dimensions.items()]
        metric_queries[0]["MetricStat"]["Metric"]["Dimensions"] = dims

    if unit:
        metric_queries[0]["MetricStat"]["Metric"]["Unit"] = unit

    params = {
        "StartTime": start_time,
        "EndTime": end_time,
        "MetricDataQueries": metric_queries,
        "ScanBy": "TimestampDescending",
    }

    response = client.get_metric_data(**params)
    normalized = normalize_cloudwatch_response(response)

    all_datapoints = []
    for result in normalized:
        timestamps = result.get("timestamps", [])
        values = result.get("values", [])
        for ts, val in zip(timestamps, values):
            dp = MetricDataPoint(
                timestamp=ts,
                value=val,
                unit=unit or "None",
            )
            all_datapoints.append(dp)

    return sorted(all_datapoints, key=lambda p: p.timestamp)


def query_metric_window_simple(
    metric_name: str,
    namespace: str,
    duration_minutes: int = 60,
    period: int = 60,
) -> List[MetricDataPoint]:
    """
    Simple wrapper that queries the last N minutes of metric data.

    Args:
        metric_name: CloudWatch metric name
        namespace: CloudWatch namespace
        duration_minutes: Number of recent minutes to query
        period: Data point interval in seconds

    Returns:
        List of MetricDataPoint objects.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)
    return query_metric_window(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period,
    )
