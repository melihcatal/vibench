from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

import boto3



def archive_document_snapshots(records: Iterable[Dict[str, Any]], bucket_name: str, prefix: str = "exports/", snapshot_name: Optional[str] = None) -> Dict[str, Any]:
    s3 = boto3.client("s3")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    object_key = f"{prefix}{snapshot_name or 'document-snapshot'}-{timestamp}.json"
    body = json.dumps(list(records), ensure_ascii=False, indent=2).encode("utf-8")
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
        ContentType="application/json",
    )
    return {
        "provider": "amazon-s3",
        "bucket": bucket_name,
        "key": object_key,
        "size_bytes": len(body),
    }
