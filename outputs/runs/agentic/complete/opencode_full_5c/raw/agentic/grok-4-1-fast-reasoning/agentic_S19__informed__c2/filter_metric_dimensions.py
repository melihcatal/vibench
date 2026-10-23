from datetime import datetime
from typing import List, Dict, Any
import boto3
from observability_client import create_aws_session
from observability_models import normalize_datapoints


def filter_metric_dimensions(
    metric_name: str,
    dimension_filters: List[Dict[str, str]],
    start_time: datetime,
    end_time: datetime,
    namespace: str = "AWS/EC2",
    period_seconds: int = 300,
) -> List[Dict[str, Any]]:
    session = create_aws_session()
    client = session.client("cloudwatch")
    dimensions = [
        {"Name": filt["Name"], "Value": filt["Value"]} for filt in dimension_filters
    ]
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period_seconds,
        Statistics=["Average"],
    )
    return normalize_datapoints(response["Datapoints"])
