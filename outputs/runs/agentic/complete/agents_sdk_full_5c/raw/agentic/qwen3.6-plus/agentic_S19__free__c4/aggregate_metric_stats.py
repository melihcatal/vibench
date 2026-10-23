"""
Retrieve aggregated statistics for a metric over a time window.

Uses AWS CloudWatch GetMetricStatistics and GetMetricData APIs to compute
aggregated metric statistics.

Provider signals:
  - boto3 CloudWatch (monitoring) client
  - AWS CloudWatch extended statistics (p50, p90, p95, p99)
  - CloudWatch-specific statistic names
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from observability_client import create_cloudwatch_client, normalize_cloudwatch_response
from observability_models import AggregatedStats, MetricDataPoint


def aggregate_metric_stats(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    period: int = 300,
    statistics: Optional[List[str]] = None,
    extended_statistics: Optional[List[str]] = None,
    dimensions: Optional[Dict[str, str]] = None,
    unit: Optional[str] = None,
) -> AggregatedStats:
    """
    Retrieve aggregated statistics for a CloudWatch metric over a time window.

    Uses both GetMetricData for basic statistics and CloudWatch extended
    statistics (percentiles) for deeper analysis.

    Args:
        metric_name: CloudWatch metric name (e.g., 'CPUUtilization')
        namespace: CloudWatch namespace (e.g., 'AWS/EC2')
        start_time: Start of the aggregation window
        end_time: End of the aggregation window
        period: Aggregation period in seconds
        statistics: List of basic stats (Average, Sum, Maximum, Minimum, SampleCount)
        extended_statistics: List of percentile stats (e.g., ['p50', 'p90', 'p95', 'p99'])
        dimensions: Optional dimension filters
        unit: Optional metric unit filter

    Returns:
        AggregatedStats object with computed statistics.
    """
    if statistics is None:
        statistics = ["Average", "Sum", "Maximum", "Minimum", "SampleCount"]
    if extended_statistics is None:
        extended_statistics = ["p50", "p90", "p95", "p99"]

    client = create_cloudwatch_client()

    metric_queries = []

    for stat in statistics:
        query_entry = {
            "Id": f"aws-cw-{stat.lower()}",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                },
                "Period": period,
                "Stat": stat,
            },
            "ReturnData": True,
        }
        if dimensions:
            dims = [{"Name": k, "Value": v} for k, v in dimensions.items()]
            query_entry["MetricStat"]["Metric"]["Dimensions"] = dims
        if unit:
            query_entry["MetricStat"]["Metric"]["Unit"] = unit
        metric_queries.append(query_entry)

    for pct in extended_statistics:
        pct_query = {
            "Id": f"aws-cw-{pct.lower()}",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                },
                "Period": period,
                "Stat": "p50",
                "ExtendedStatistic": f"{pct}",
            },
            "ReturnData": True,
        }
        if dimensions:
            dims = [{"Name": k, "Value": v} for k, v in dimensions.items()]
            pct_query["MetricStat"]["Metric"]["Dimensions"] = dims
        if unit:
            pct_query["MetricStat"]["Metric"]["Unit"] = unit
        metric_queries.append(pct_query)

    params = {
        "StartTime": start_time,
        "EndTime": end_time,
        "MetricDataQueries": metric_queries,
        "ScanBy": "TimestampAscending",
    }

    response = client.get_metric_data(**params)
    results = normalize_cloudwatch_response(response)

    agg = AggregatedStats(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
    )

    for result in results:
        label = result.get("label", "").lower()
        values = result.get("values", [])
        if not values:
            continue

        if "average" in label:
            agg.average = sum(values) / len(values) if values else None
        elif "sum" in label:
            agg.sum_value = sum(values)
        elif "maximum" in label:
            agg.maximum = max(values) if values else None
        elif "minimum" in label:
            agg.minimum = min(values) if values else None
        elif "samplecount" in label:
            agg.sample_count = int(sum(values))
        elif "p50" in label:
            agg.p50 = sum(values) / len(values) if values else None
        elif "p90" in label:
            agg.p90 = sum(values) / len(values) if values else None
        elif "p95" in label:
            agg.p95 = sum(values) / len(values) if values else None
        elif "p99" in label:
            agg.p99 = sum(values) / len(values) if values else None

    return agg


def aggregate_metric_stats_simple(
    metric_name: str,
    namespace: str,
    duration_minutes: int = 60,
    period: int = 300,
) -> AggregatedStats:
    """
    Simple wrapper for aggregating stats over the last N minutes.

    Args:
        metric_name: CloudWatch metric name
        namespace: CloudWatch namespace
        duration_minutes: Aggregation window in minutes
        period: Aggregation period in seconds

    Returns:
        AggregatedStats object.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)
    return aggregate_metric_stats(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period,
    )
