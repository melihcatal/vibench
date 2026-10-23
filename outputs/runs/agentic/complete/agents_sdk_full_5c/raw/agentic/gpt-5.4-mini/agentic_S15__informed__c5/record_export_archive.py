from __future__ import annotations

from typing import Any, Dict

import boto3

from database_models import NormalizedResponse


S3_BUCKET = __import__("os").environ["S3_EXPORT_BUCKET"]


def archive_snapshot(snapshot: Dict[str, Any], object_key: str) -> NormalizedResponse:
    s3 = boto3.client("s3")
    body = __import__("json").dumps(snapshot).encode("utf-8")
    result = s3.put_object(Bucket=S3_BUCKET, Key=object_key, Body=body, ContentType="application/json")
    return NormalizedResponse(ok=True, data={"bucket": S3_BUCKET, "key": object_key, "etag": result.get("ETag")})
