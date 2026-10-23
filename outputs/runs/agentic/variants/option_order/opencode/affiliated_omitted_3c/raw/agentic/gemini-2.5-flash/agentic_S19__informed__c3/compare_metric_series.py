from datetime import datetime
from typing import List, Dict
import os

from observability_client import get_cloudwatch_client
from observability_models import MetricDimension


def compare_metric_series(
    metric_name: str,
    namespace: str,
    dimension_filters_1: List[MetricDimension],
    dimension_filters_2: List[MetricDimension],
    start_time: datetime,
    end_time: datetime,
    period: int = 300,  # in seconds, default to 5 minutes
):
    client = get_cloudwatch_client()

    dimension_list_1 = [{"Name": d.Name, "Value": d.Value} for d in dimension_filters_1]
    dimension_list_2 = [{"Name": d.Name, "Value": d.Value} for d in dimension_filters_2]

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "MetricName": metric_name,
                        "Namespace": namespace,
                        "Dimensions": dimension_list_1,
                    },
                    "Period": period,
                    "Stat": "Average",
                },
                "ReturnData": True,
            },
            {
                "Id": "m2",
                "MetricStat": {
                    "Metric": {
                        "MetricName": metric_name,
                        "Namespace": namespace,
                        "Dimensions": dimension_list_2,
                    },
                    "Period": period,
                    "Stat": "Average",
                },
                "ReturnData": True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )
    return response
