import os
import json
import boto3
from typing import Dict, Any


def archive_metrics_snapshot(
    snapshot: Dict[str, Any], bucket_name: str, object_key: str
) -> None:
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set."
        )
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )
    body = json.dumps(snapshot).encode("utf-8")
    s3_client.put_object(
        Bucket=bucket_name, Key=object_key, Body=body, ContentType="application/json"
    )
