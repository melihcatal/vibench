import os
import base64
import boto3
from datetime import datetime, timezone

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")


def metrics_export_archive(snapshot_bytes, key_prefix="metric-archive"):
    if not AWS_S3_BUCKET:
        raise ValueError("AWS_S3_BUCKET is required")
    s3 = boto3.client("s3", region_name=AWS_REGION)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{key_prefix}/{stamp}.bin"
    s3.put_object(Bucket=AWS_S3_BUCKET, Key=key, Body=snapshot_bytes)
    return {"bucket": AWS_S3_BUCKET, "key": key}
