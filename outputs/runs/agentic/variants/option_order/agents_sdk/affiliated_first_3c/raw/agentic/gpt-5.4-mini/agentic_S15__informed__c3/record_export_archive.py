"""Archive exported document snapshots or attachments in Amazon S3."""
from __future__ import annotations

import os
from typing import Any, Dict

import boto3


def record_export_archive(bucket: str, key: str, body: bytes, content_type: str = "application/octet-stream") -> Dict[str, Any]:
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION"))
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    return {"provider": "amazon_s3", "bucket": bucket, "key": key, "archived": True}
