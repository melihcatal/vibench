import boto3
import os
from datetime import datetime, timedelta
from typing import Dict, Any


def key_usage_summary(key_id: str, hours: int = 24) -> Dict[str, Any]:
    region = os.getenv("AWS_REGION", "us-east-1")
    cw_client = boto3.client("cloudwatch", region_name=region)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    dimensions = [{"Name": "KeyId", "Value": key_id}]
    metric_requests = cw_client.get_metric_statistics(
        Namespace="AWS/KMS",
        MetricName="NumberOfRequests",
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=["Sum", "Average"],
    )
    metric_bytes_enc = cw_client.get_metric_statistics(
        Namespace="AWS/KMS",
        MetricName="BytesEncrypted",
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=["Sum", "Average"],
    )
    return {
        "requests": metric_requests.get("Datapoints", []),
        "bytes_encrypted": metric_bytes_enc.get("Datapoints", []),
    }
