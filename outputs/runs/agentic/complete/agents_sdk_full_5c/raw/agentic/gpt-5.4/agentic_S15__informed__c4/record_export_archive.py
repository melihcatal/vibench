from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

import boto3


def archive_document_snapshots(records: Iterable[Dict[str, Any]], archive_prefix: str = "exports/", bucket: Optional[str] = None) -> Dict[str, Any]:
    s3 = boto3.client("s3")
    bucket_name = bucket or os.environ["S3_ARCHIVE_BUCKET"]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_key = f"{archive_prefix}document-snapshot-{timestamp}.json"
    body = json.dumps(list(records), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
        ContentType="application/json",
    )
    return {
        "provider": "Amazon S3",
        "bucket": bucket_name,
        "key": object_key,
        "size_bytes": len(body),
    }
