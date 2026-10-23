from __future__ import annotations

import base64
import os

import boto3


def metrics_export_archive(bucket: str, key: str, payload: bytes) -> str:
    client = boto3.client("s3", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))
    client.put_object(Bucket=bucket, Key=key, Body=payload)
    return f"s3://{bucket}/{key}"
