import boto3
import os
from typing import List, Dict, Optional
from datetime import datetime
from observability_client import get_time_window, get_aws_region
from observability_models import MetricDatapoints, Dimension


def compare_metric_series(
    metric_name: str,
    dimensions1: Optional[List[Dimension]] = None,
    dimensions2: Optional[List[Dimension]] = None,
    namespace: str = "AWS/EC2",
    window_minutes: int = 60,
    period: int = 300,
    statistics: List[str] = ["Average"],
) -> Dict[str, MetricDatapoints]:
    region = get_aws_region()
    client = boto3.client(
        "cloudwatch",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    start, end = get_time_window(window_minutes)
    dims1 = dimensions1 or []
    dims2 = dimensions2 or []
    resp1 = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dims1,
        StartTime=start,
        EndTime=end,
        Period=period,
        Statistics=statistics,
    )
    resp2 = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dims2,
        StartTime=start,
        EndTime=end,
        Period=period,
        Statistics=statistics,
    )
    return {"series1": resp1["Datapoints"], "series2": resp2["Datapoints"]}
