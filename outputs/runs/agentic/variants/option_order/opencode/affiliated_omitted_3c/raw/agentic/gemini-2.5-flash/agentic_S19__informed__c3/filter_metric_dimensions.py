from datetime import datetime
from typing import List, Dict
import os

from observability_client import get_cloudwatch_client
from observability_models import MetricDimension


def filter_metric_dimensions(
    metric_name: str,
    namespace: str,
    dimensions: List[MetricDimension],
    start_time: datetime,
    end_time: datetime,
    period: int = 300,  # in seconds, default to 5 minutes
):
    client = get_cloudwatch_client()

    dimension_list = [{"Name": d.Name, "Value": d.Value} for d in dimensions]

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "MetricName": metric_name,
                        "Namespace": namespace,
                        "Dimensions": dimension_list,
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
