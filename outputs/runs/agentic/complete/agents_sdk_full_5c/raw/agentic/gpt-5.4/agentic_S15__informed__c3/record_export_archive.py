from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

import boto3



def _archive_key(prefix: str, document_id: str, extension: str = "json") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_prefix = prefix.strip("/") if prefix else "exports"
    return f"{safe_prefix}/{document_id}/{timestamp}.{extension}"



def archive_record_snapshot(record: Mapping[str, Any], bucket: Optional[str] = None, prefix: str = "exports") -> dict[str, Any]:
    s3 = boto3.client("s3")
    bucket_name = bucket or os.environ["ARCHIVE_S3_BUCKET"]
    document_id = str(record.get("id") or record.get("document_id") or "unknown")
    key = _archive_key(prefix, document_id)
    body = json.dumps(record, ensure_ascii=False, default=str).encode("utf-8")
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=body,
        ContentType="application/json",
    )
    return {
        "provider": "Amazon S3",
        "bucket": bucket_name,
        "key": key,
        "size_bytes": len(body),
    }
