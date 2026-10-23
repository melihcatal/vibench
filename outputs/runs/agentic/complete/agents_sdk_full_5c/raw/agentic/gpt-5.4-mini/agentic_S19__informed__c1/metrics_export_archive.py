from __future__ import annotations

import os
from datetime import datetime, timezone

import boto3

from observability_models import ArchiveResult

S3_BUCKET_ENV = "METRICS_EXPORT_BUCKET"


def archive_metric_snapshot(snapshot_json: str, key_prefix: str = "metrics") -> ArchiveResult:
    bucket = os.environ[S3_BUCKET_ENV]
    s3 = boto3.client("s3")
    key = f"{key_prefix}/{datetime.now(timezone.utc).strftime('%Y/%m/%d/%H%M%S')}.json"
    response = s3.put_object(Bucket=bucket, Key=key, Body=snapshot_json.encode("utf-8"), ContentType="application/json")
    return ArchiveResult(bucket=bucket, key=key, etag=response.get("ETag"), uri=f"s3://{bucket}/{key}", raw=response)
