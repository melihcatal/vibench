from __future__ import annotations

import os
from datetime import datetime, timezone

import boto3

from observability_models import ArchiveResult


def metrics_export_archive(bucket: str, metric_name: str, payload: bytes) -> ArchiveResult:
    s3 = boto3.client("s3")
    key = f"metrics/{metric_name}/{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    response = s3.put_object(Bucket=bucket, Key=key, Body=payload, ContentType="application/json")
    return ArchiveResult(bucket=bucket, object_key=key, etag=response.get("ETag"), url=f"s3://{bucket}/{key}")
