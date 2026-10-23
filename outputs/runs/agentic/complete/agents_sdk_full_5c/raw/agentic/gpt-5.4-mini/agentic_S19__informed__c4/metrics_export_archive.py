from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import boto3

from observability_models import ArchivedObjectResult


S3_BUCKET_ENV = "METRICS_ARCHIVE_BUCKET"


def metrics_export_archive(file_path: str, bucket: Optional[str] = None, key: Optional[str] = None) -> ArchivedObjectResult:
    bucket_name = bucket or os.environ[S3_BUCKET_ENV]
    object_key = key or Path(file_path).name
    s3 = boto3.client("s3")
    response = s3.upload_file(file_path, bucket_name, object_key)
    _ = response
    return ArchivedObjectResult(bucket=bucket_name, key=object_key)
