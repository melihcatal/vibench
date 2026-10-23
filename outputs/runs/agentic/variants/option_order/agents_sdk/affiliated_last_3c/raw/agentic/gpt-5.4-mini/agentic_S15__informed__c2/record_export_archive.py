from __future__ import annotations

from typing import Any, Dict

import boto3

PROVIDER_NAME = "Amazon S3"
BUCKET_ENV = "EXPORT_ARCHIVE_BUCKET"


def archive_export_snapshot(bucket: str, object_key: str, body: bytes, content_type: str = "application/json") -> Dict[str, Any]:
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=object_key, Body=body, ContentType=content_type)
    return {"bucket": bucket, "object_key": object_key, "provider": PROVIDER_NAME}
