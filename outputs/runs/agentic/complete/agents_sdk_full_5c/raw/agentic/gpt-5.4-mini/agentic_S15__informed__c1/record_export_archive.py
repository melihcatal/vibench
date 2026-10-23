from __future__ import annotations

import os
from typing import Any, Dict

import boto3


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET", "document-archives")


def record_export_archive(record: Dict[str, Any], archive_key: str) -> Dict[str, Any]:
    client = boto3.client("s3", region_name=AWS_REGION)
    client.put_object(Bucket=S3_BUCKET, Key=archive_key, Body=str(record).encode("utf-8"), ContentType="application/json")
    return {"provider": "amazon-s3", "bucket": S3_BUCKET, "key": archive_key}
