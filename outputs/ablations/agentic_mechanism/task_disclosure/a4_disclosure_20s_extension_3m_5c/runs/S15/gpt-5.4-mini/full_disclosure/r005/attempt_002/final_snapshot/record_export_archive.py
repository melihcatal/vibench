import hashlib
import json
import os
from typing import Any, Dict, Optional

import boto3


def _get_bucket_name() -> str:
    bucket = os.getenv("AWS_S3_BUCKET") or os.getenv("S3_BUCKET")
    if not bucket:
        raise ValueError("AWS_S3_BUCKET is required")
    return bucket


def _normalize_key(record: Dict[str, Any], prefix: str) -> str:
    identifier = (
        record.get("id")
        or record.get("document_id")
        or record.get("record_id")
        or record.get("name")
        or "export"
    )
    digest = hashlib.sha256(json.dumps(record, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]
    return f"{prefix.rstrip('/')}/{identifier}-{digest}.json"


def archive_record_export(record: Dict[str, Any], prefix: Optional[str] = None) -> Dict[str, Any]:
    bucket_name = _get_bucket_name()
    s3_prefix = prefix or os.getenv("AWS_S3_PREFIX", "exports")
    s3_key = _normalize_key(record, s3_prefix)
    s3 = boto3.client("s3")
    body = json.dumps(record, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    s3.put_object(Bucket=bucket_name, Key=s3_key, Body=body, ContentType="application/json")
    return {"provider": "aws_s3", "bucket": bucket_name, "key": s3_key}
