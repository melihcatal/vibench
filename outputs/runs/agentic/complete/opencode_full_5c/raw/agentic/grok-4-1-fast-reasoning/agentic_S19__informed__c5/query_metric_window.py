import boto3
import os
from datetime import datetime
from typing import List
from observability_models import (
    MetricQuery,
    TimeWindow,
    MetricDatapoint,
    Dimension,
    MetricResponse,
)
from observability_client import parse_time_window, normalize_get_metric_data


def query_metric_window(
    metric_query: MetricQuery, time_window: TimeWindow, period_seconds: int = 300
) -> MetricResponse:
    client = boto3.client(
        "cloudwatch",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    start, end = parse_time_window(time_window)
    dims = [{"Name": d.name, "Value": d.value} for d in metric_query.dimensions or []]
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "q1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": metric_query.namespace,
                        "MetricName": metric_query.metric_name,
                        "Dimensions": dims,
                    },
                    "Period": period_seconds,
                    "Stat": "Average",
                },
            }
        ],
        StartTime=start,
        EndTime=end,
    )
    result = response["MetricDataResults"][0]
    datapoints = normalize_get_metric_data(result)
    return MetricResponse(query=metric_query, datapoints=datapoints)
