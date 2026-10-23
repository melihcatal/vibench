import datetime
from typing import List, Dict, Any
import os

from observability_client import get_cloudwatch_client  # AWS boto3 client
from observability_models import MetricDataResult, MetricDataPoint


def filter_metric_dimensions(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int,
    statistics: List[str],
    dimensions: List[Dict[str, str]],
) -> List[MetricDataResult]:
    """Queries metric data filtered by resource labels or dimensions using AWS CloudWatch.

    Args:
        namespace (str): The namespace of the metric (e.g., 'AWS/EC2').
        metric_name (str): The name of the metric (e.g., 'CPUUtilization').
        start_time (datetime.datetime): The start of the time window.
        end_time (datetime.datetime): The end of the time window.
        period (int): The granularity, in seconds (e.g., 300 for 5 minutes).
        statistics (List[str]): The statistics to retrieve (e.g., ['Average', 'Maximum']).
        dimensions (List[Dict[str, str]]): A list of dimensions to filter the metric data.
                                            Must not be empty for filtering.

    Returns:
        List[MetricDataResult]: A list of metric data results matching the dimensions.
    """
    if not dimensions:
        raise ValueError("Dimensions must be provided to filter metric data.")

    cloudwatch = get_cloudwatch_client()

    metric_data_queries = [
        {
            "Id": f"m{idx}",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": metric_name,
                    "Dimensions": dimensions,
                },
                "Period": period,
                "Stat": stat,
            },
            "ReturnData": True,
        }
        for idx, stat in enumerate(statistics)
    ]

    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_data_queries, StartTime=start_time, EndTime=end_time
    )

    results: List[MetricDataResult] = []
    for result in response.get("MetricDataResults", []):
        datapoints: List[MetricDataPoint] = []
        timestamps = result.get("Timestamps", [])
        values = result.get("Values", [])

        for i in range(len(timestamps)):
            unit = result.get("Unit", "None")
            datapoints.append(
                {"timestamp": timestamps[i], "value": float(values[i]), "unit": unit}
            )
        results.append(
            {"label": result.get("Label", "Unknown"), "datapoints": datapoints}
        )

    return results
