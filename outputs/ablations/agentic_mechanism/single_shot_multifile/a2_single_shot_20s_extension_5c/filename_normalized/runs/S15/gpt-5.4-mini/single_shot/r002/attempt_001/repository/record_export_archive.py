from __future__ import annotations

import os
from typing import Any, Dict

import boto3

from database_models import success_response, error_response

S3_BUCKET = os.getenv("EXPORT_ARCHIVE_BUCKET", "")


async def record_export_archive(request: Dict[str, Any]) -> Dict[str, Any]:
    key = request.get("key")
    body = request.get("body", "")
    if not isinstance(key, str) or not key:
        return error_response("key is required")
    if not S3_BUCKET:
        return error_response("EXPORT_ARCHIVE_BUCKET is required", code="missing_config")
    s3 = boto3.client("s3")
    try:
        s3.put_object(Bucket=S3_BUCKET, Key=key, Body=body if isinstance(body, (bytes, bytearray)) else str(body).encode("utf-8"))
        return success_response({"bucket": S3_BUCKET, "key": key})
    except Exception as exc:
        return error_response(str(exc), code="provider_error")