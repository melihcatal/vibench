from __future__ import annotations

import json
from typing import Any, Dict

import boto3

from database_models import ExportArchiveResult


S3_BUCKET_ENV = "DOCUMENT_EXPORT_BUCKET"


def archive_record_snapshot(record: Dict[str, Any], bucket: str, key_prefix: str = "exports/") -> ExportArchiveResult:
    s3 = boto3.client("s3")
    document_id = str(record.get("document_id", "document"))
    key = f"{key_prefix.rstrip('/')}/{document_id}.json"
    body = json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    url = f"s3://{bucket}/{key}"
    return ExportArchiveResult(document_id=document_id, bucket=bucket, key=key, url=url)
