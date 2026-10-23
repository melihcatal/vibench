from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from boto3 import client as boto3_client


def record_export_archive(
    document: dict[str, Any], bucket: str, prefix: str = "exports"
) -> dict[str, Any]:
    s3 = boto3_client("s3")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    document_id = str(document.get("id", "document"))
    key = f"{prefix.rstrip('/')}/{document_id}-{timestamp}.json"
    body = json.dumps(document, ensure_ascii=False, default=str).encode("utf-8")
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="application/json",
        Metadata={"provider": "amazon-s3", "document-id": document_id},
    )
    return {
        "provider": "amazon_s3",
        "bucket": bucket,
        "key": key,
        "size": len(body),
    }
