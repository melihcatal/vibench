import boto3
import os
from typing import List
from datetime import datetime
from observability_client import get_time_window, get_aws_region
from observability_models import MetricDatapoints, Dimension


def filter_metric_dimensions(
    metric_name: str,
    dimensions: List[Dimension],
    namespace: str = "AWS/EC2",
    window_minutes: int = 60,
    period: int = 300,
    statistics: List[str] = ["Average"],
) -> MetricDatapoints:
    region = get_aws_region()
    client = boto3.client(
        "cloudwatch",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    start, end = get_time_window(window_minutes)
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start,
        EndTime=end,
        Period=period,
        Statistics=statistics,
    )
    return response["Datapoints"]
