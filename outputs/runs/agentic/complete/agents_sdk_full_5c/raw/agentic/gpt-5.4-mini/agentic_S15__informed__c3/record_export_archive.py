from __future__ import annotations

from typing import Any, Dict

import boto3

S3_SERVICE = "Amazon S3"


def archive_snapshot(bucket: str, key: str, body: bytes, content_type: str = "application/json") -> Dict[str, Any]:
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    return {"bucket": bucket, "key": key, "service": S3_SERVICE}
