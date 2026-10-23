from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


AWS_S3_SERVICE = "s3"


def metrics_export_archive(
    snapshot: Dict[str, Any],
    bucket_name: str,
    key_prefix: str = "metric-exports",
    region_name: Optional[str] = None,
) -> Dict[str, str]:
    s3 = boto3.client(AWS_S3_SERVICE, region_name=region_name or os.getenv("AWS_REGION") or "us-east-1")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_key = f"{key_prefix.rstrip('/')}/metrics-{timestamp}.json"
    body = json.dumps(snapshot, separators=(",", ":")).encode("utf-8")
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
        ContentType="application/json",
    )
    return {
        "bucket": bucket_name,
        "key": object_key,
        "uri": f"s3://{bucket_name}/{object_key}",
    }
