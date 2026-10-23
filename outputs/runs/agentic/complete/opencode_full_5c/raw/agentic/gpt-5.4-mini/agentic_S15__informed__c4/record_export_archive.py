import os
from typing import Any

import boto3


def record_export_archive(
    key: str, body: bytes, content_type: str = "application/octet-stream"
) -> str:
    bucket = os.getenv("AWS_S3_BUCKET")
    if not bucket:
        raise RuntimeError("AWS_S3_BUCKET is required")
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    return f"s3://{bucket}/{key}"
