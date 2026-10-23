from __future__ import annotations

from typing import Any, Dict

import boto3

from database_models import as_iso_utc


S3_BUCKET_ENV = "AWS_S3_EXPORT_BUCKET"


def archive_record_snapshot(snapshot: Dict[str, Any], object_key: str) -> Dict[str, Any]:
    bucket = __import__("os").environ[S3_BUCKET_ENV]
    s3 = boto3.client("s3")
    body = __import__("json").dumps(snapshot, sort_keys=True).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=object_key, Body=body, ContentType="application/json")
    return {"provider": "boto3-s3", "bucket": bucket, "key": object_key, "archived_at": as_iso_utc()}
