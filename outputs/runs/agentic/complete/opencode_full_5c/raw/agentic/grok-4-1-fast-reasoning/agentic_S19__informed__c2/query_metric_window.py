from datetime import datetime, timedelta
from typing import List, Dict, Any
import boto3
from observability_client import create_aws_session
from observability_models import normalize_datapoints


def query_metric_window(
    metric_name: str,
    window_minutes: int = 60,
    namespace: str = "AWS/EC2",
    period_seconds: int = 300,
) -> List[Dict[str, Any]]:
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=window_minutes)
    session = create_aws_session()
    client = session.client("cloudwatch")
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period_seconds,
        Statistics=["Average"],
    )
    return normalize_datapoints(response["Datapoints"])
