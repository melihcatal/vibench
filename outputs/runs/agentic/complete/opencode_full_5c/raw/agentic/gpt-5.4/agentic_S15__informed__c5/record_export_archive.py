from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import boto3


def archive_record_snapshot(
    record: dict[str, Any], bucket_name: str, object_prefix: str = "document-archive"
) -> dict[str, Any]:
    s3_client = boto3.client("s3")
    document_id = str(record.get("id") or record.get("document_id") or "unknown")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{object_prefix.rstrip('/')}/{document_id}-{timestamp}.json"
    payload = json.dumps(record, ensure_ascii=False).encode("utf-8")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=payload,
        ContentType="application/json",
    )
    return {
        "provider": "amazon-s3",
        "bucket": bucket_name,
        "key": key,
        "size": len(payload),
    }
