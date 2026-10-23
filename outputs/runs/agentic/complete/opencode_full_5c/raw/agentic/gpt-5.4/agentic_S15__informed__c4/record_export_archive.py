from __future__ import annotations

import os
from typing import Any

import boto3

from database_models import canonical_json


def archive_record_snapshot(
    record: dict[str, Any], archive_key: str, content_type: str = "application/json"
) -> dict[str, Any]:
    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    bucket = os.environ.get("S3_ARCHIVE_BUCKET")
    s3 = boto3.client("s3", region_name=region)
    body = canonical_json(record).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=archive_key, Body=body, ContentType=content_type)
    return {
        "provider": "amazon_s3",
        "bucket": bucket,
        "key": archive_key,
        "size_bytes": len(body),
    }
