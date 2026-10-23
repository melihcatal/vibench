import boto3
from datetime import datetime, timedelta
import os


def key_usage_summary(key_id: str, hours: int = 24) -> dict:
    cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    metrics = ["NumberOfBytesEncrypted", "NumberOfBytesDecrypted", "RequestCount"]
    summary = {}
    for metric in metrics:
        resp = cloudwatch.get_metric_statistics(
            Namespace="AWS/KMS",
            MetricName=metric,
            Dimensions=[{"Name": "KeyId", "Value": key_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Sum", "Average", "SampleCount"],
        )
        summary[metric] = resp.get("Datapoints", [])
    return summary
