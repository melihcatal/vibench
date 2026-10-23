import boto3
from typing import List, Dict, Any, Optional
from observability_client import get_aws_region, make_dimensions, create_recent_window
from observability_models import parse_datapoints, MetricDatapoint


def query_metric_window(
    metric_name: str,
    duration_minutes: int = 60,
    namespace: str = "AWS/EC2",
    period: int = 300,
    statistics: List[str] = ["Average"],
    dimensions: Optional[List[Dict[str, str]]] = None,
) -> List[MetricDatapoint]:
    region = get_aws_region()
    client = boto3.client("cloudwatch", region_name=region)
    window = create_recent_window(duration_minutes)
    dims = make_dimensions(dimensions)
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=window["start"],
        EndTime=window["end"],
        Period=period,
        Statistics=statistics,
        Dimensions=dims,
    )
    return parse_datapoints(response["Datapoints"])
