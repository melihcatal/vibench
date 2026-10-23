import datetime
from typing import List, Dict, Any, Optional
import os

from observability_client import get_cloudwatch_client  # AWS boto3 client
from observability_models import AggregatedMetricStats


def aggregate_metric_stats(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int,
    statistics: List[str],
    dimensions: List[Dict[str, str]] = None,
) -> List[AggregatedMetricStats]:
    """Retrieves aggregated statistics for a metric over a time window using AWS CloudWatch.

    Args:
        namespace (str): The namespace of the metric (e.g., 'AWS/EC2').
        metric_name (str): The name of the metric (e.g., 'CPUUtilization').
        start_time (datetime.datetime): The start of the time window.
        end_time (datetime.datetime): The end of the time window.
        period (int): The granularity, in seconds (e.g., 300 for 5 minutes).
        statistics (List[str]): The statistics to retrieve (e.g., ['Average', 'Maximum']).
        dimensions (List[Dict[str, str]], optional): A list of dimensions to filter the metric data.

    Returns:
        List[AggregatedMetricStats]: A list of aggregated metric statistics.
    """
    cloudwatch = get_cloudwatch_client()

    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions or [],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics,
    )

    results: List[AggregatedMetricStats] = []
    for dp in response.get("Datapoints", []):
        results.append(
            {
                "timestamp": dp.get("Timestamp"),
                "average": dp.get("Average"),
                "sum": dp.get("Sum"),
                "unit": dp.get("Unit"),
            }
        )

    return results
