from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Iterable

import boto3



def archive_document_snapshots(records: Iterable[Dict[str, Any]], bucket_name: str, prefix: str = "exports") -> str:
    s3_client = boto3.client("s3")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{prefix}/document-snapshot-{timestamp}.json"
    body = json.dumps([dict(record) for record in records], ensure_ascii=False, indent=2).encode("utf-8")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=body,
        ContentType="application/json",
    )
    return f"s3://{bucket_name}/{key}"
