from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import boto3


AWS_S3_STORAGE_CLASS = "STANDARD"


def metrics_export_archive(snapshot: Dict[str, Any], bucket: str, prefix: str = "metrics-archives") -> Dict[str, str]:
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    s3 = boto3.client("s3", region_name=region)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{prefix.rstrip('/')}/snapshot-{timestamp}.json"
    body = json.dumps(snapshot, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="application/json",
        StorageClass=AWS_S3_STORAGE_CLASS,
    )
    return {
        "provider": "Amazon S3",
        "bucket": bucket,
        "key": key,
        "region": region,
    }
