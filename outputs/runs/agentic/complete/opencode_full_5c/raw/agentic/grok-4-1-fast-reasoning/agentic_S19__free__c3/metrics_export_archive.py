import boto3
import os
import json
from typing import Any, Dict


def archive_metrics_snapshot(
    metrics_data: Dict[str, Any], bucket_name: str, object_key: str
):
    region = os.getenv("AWS_REGION", "us-east-1")
    s3_client = boto3.client("s3", region_name=region)
    data_str = json.dumps(metrics_data, default=str, indent=2)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=data_str,
        ContentType="application/json",
    )
