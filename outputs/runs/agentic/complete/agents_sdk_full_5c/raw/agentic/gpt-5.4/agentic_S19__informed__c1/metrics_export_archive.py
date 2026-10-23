from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import boto3


DEFAULT_S3_BUCKET = os.getenv("METRIC_ARCHIVE_S3_BUCKET")
DEFAULT_S3_PREFIX = os.getenv("METRIC_ARCHIVE_S3_PREFIX", "metrics-exports/")



def metrics_export_archive(snapshot: Dict[str, Any], bucket: str | None = None, key_prefix: str | None = None) -> Dict[str, Any]:
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    bucket_name = bucket or DEFAULT_S3_BUCKET
    prefix = key_prefix or DEFAULT_S3_PREFIX
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_key = f"{prefix.rstrip('/')}/metric-snapshot-{timestamp}.json"
    body = json.dumps(snapshot, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
        ContentType="application/json",
    )
    return {
        "provider": "Amazon S3",
        "bucket": bucket_name,
        "key": object_key,
        "bytes": len(body),
    }
