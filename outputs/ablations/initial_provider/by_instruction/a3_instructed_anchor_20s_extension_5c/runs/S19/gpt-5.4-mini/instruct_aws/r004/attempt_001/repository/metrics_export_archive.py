import os
from typing import Dict

import boto3


def metrics_export_archive(bucket: str, key: str, body: bytes) -> Dict[str, str]:
    client = boto3.client("s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key, "provider": "AWS S3"}
