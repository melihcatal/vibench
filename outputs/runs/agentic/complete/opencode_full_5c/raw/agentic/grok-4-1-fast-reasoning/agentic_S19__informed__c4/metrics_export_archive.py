import os
import boto3
import json
from typing import Dict, Any


def metrics_export_archive(snapshot: Dict[str, Any], bucket_name: str, object_key: str):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(snapshot, default=str),
        ContentType="application/json",
    )
