from __future__ import annotations

import json
import os
from typing import Any, Dict

import boto3


S3_BUCKET_ENV = "ARCHIVE_S3_BUCKET"


def archive_document_snapshot(document: Dict[str, Any], object_key: str) -> str:
    bucket = os.environ[S3_BUCKET_ENV]
    s3 = boto3.client("s3")
    body = json.dumps(document, ensure_ascii=False).encode("utf-8")
    s3.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=body,
        ContentType="application/json",
    )
    return f"s3://{bucket}/{object_key}"
