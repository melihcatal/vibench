from __future__ import annotations

from typing import Optional

import boto3

from observability_models import ExportArchiveResult


S3_PROVIDER_SIGNAL = "boto3.s3"


def metrics_export_archive(bucket: str, key: str, body: bytes, content_type: str = "application/json", region_name: Optional[str] = None) -> ExportArchiveResult:
    client = boto3.client("s3", region_name=region_name)
    response = client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    etag = response.get("ETag")
    uri = f"s3://{bucket}/{key}"
    return ExportArchiveResult(bucket=bucket, key=key, etag=etag, uri=uri)
