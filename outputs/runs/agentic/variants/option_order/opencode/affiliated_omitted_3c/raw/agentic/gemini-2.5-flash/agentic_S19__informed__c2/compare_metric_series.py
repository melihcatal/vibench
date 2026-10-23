import datetime
from typing import List, Dict, Any
import os

from observability_client import get_cloudwatch_client  # AWS boto3 client
from observability_models import MetricDataResult, MetricDataPoint


def compare_metric_series(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int,
    statistics: List[str],
    series1_dimensions: List[Dict[str, str]],
    series2_dimensions: List[Dict[str, str]],
) -> Dict[str, List[MetricDataResult]]:
    """Compares metric values for two resources or dimension filters over the same window using AWS CloudWatch.

    Args:
        namespace (str): The namespace of the metric (e.g., 'AWS/EC2').
        metric_name (str): The name of the metric (e.g., 'CPUUtilization').
        start_time (datetime.datetime): The start of the time window.
        end_time (datetime.datetime): The end of the time window.
        period (int): The granularity, in seconds (e.g., 300 for 5 minutes).
        statistics (List[str]): The statistics to retrieve (e.g., ['Average', 'Maximum']).
        series1_dimensions (List[Dict[str, str]]): Dimensions for the first metric series.
        series2_dimensions (List[Dict[str, str]]): Dimensions for the second metric series.

    Returns:
        Dict[str, List[MetricDataResult]]: A dictionary containing results for 'series1' and 'series2'.
    """
    cloudwatch = get_cloudwatch_client()

    metric_data_queries = []

    # Query for series 1
    for idx, stat in enumerate(statistics):
        metric_data_queries.append(
            {
                "Id": f"s1m{idx}",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": series1_dimensions,
                    },
                    "Period": period,
                    "Stat": stat,
                },
                "ReturnData": True,
                "Label": f"Series1 {stat}",
            }
        )

    # Query for series 2
    for idx, stat in enumerate(statistics):
        metric_data_queries.append(
            {
                "Id": f"s2m{idx}",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": series2_dimensions,
                    },
                    "Period": period,
                    "Stat": stat,
                },
                "ReturnData": True,
                "Label": f"Series2 {stat}",
            }
        )

    response = cloudwatch.get_metric_data(
        MetricDataQueries=metric_data_queries, StartTime=start_time, EndTime=end_time
    )

    series_results: Dict[str, List[MetricDataResult]] = {"series1": [], "series2": []}

    for result in response.get("MetricDataResults", []):
        datapoints: List[MetricDataPoint] = []
        timestamps = result.get("Timestamps", [])
        values = result.get("Values", [])
        unit = result.get("Unit", "None")

        for i in range(len(timestamps)):
            datapoints.append(
                {"timestamp": timestamps[i], "value": float(values[i]), "unit": unit}
            )

        metric_data_result: MetricDataResult = {
            "label": result.get("Label", "Unknown"),
            "datapoints": datapoints,
        }

        if result.get("Label", "").startswith("Series1"):
            series_results["series1"].append(metric_data_result)
        elif result.get("Label", "").startswith("Series2"):
            series_results["series2"].append(metric_data_result)

    return series_results
