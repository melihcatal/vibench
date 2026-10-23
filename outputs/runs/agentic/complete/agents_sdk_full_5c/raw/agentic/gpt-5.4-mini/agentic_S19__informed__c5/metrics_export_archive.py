from __future__ import annotations

import json

import boto3

from observability_models import ArchiveRequest

PROVIDER = "Amazon S3"


def metrics_export_archive(bucket: str, key: str, payload: dict) -> dict:
    archive = ArchiveRequest(bucket=bucket, key=key, payload=json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    s3 = boto3.client("s3")
    response = s3.put_object(Bucket=archive.bucket, Key=archive.key, Body=archive.payload, ContentType=archive.content_type)
    return {"provider": PROVIDER, "etag": response.get("ETag"), "bucket": archive.bucket, "key": archive.key}
