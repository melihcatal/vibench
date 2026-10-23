from __future__ import annotations

import base64
import json
from datetime import datetime, timezone
from typing import Any, Dict

import boto3

S3_BUCKET_ENV = "METRICS_EXPORT_S3_BUCKET"
S3_PREFIX_ENV = "METRICS_EXPORT_S3_PREFIX"


def metrics_export_archive(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    bucket = __import__("os").environ.get(S3_BUCKET_ENV, "")
    if not bucket:
        raise RuntimeError("METRICS_EXPORT_S3_BUCKET is required for Amazon S3 archiving")
    prefix = __import__("os").environ.get(S3_PREFIX_ENV, "metrics-archive")
    s3 = boto3.client("s3")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{prefix.rstrip('/')}/{name}-{ts}.json"
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": key, "etag": base64.b64encode(key.encode()).decode(), "bytes": len(body)}
