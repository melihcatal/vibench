from __future__ import annotations

import json
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional

import boto3


def archive_record_snapshot(
    document: Dict[str, Any],
    bucket_name: str,
    object_prefix: str = "records",
    attachment_bytes: Optional[bytes] = None,
    attachment_name: Optional[str] = None,
) -> Dict[str, str]:
    s3_client = boto3.client("s3")
    document_id = str(document["id"])
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    snapshot_key = f"{object_prefix}/{document_id}/{timestamp}.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=snapshot_key,
        Body=json.dumps(document, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json",
    )
    result = {"provider": "Amazon S3", "snapshot_key": snapshot_key}
    if attachment_bytes is not None and attachment_name:
        attachment_key = f"{object_prefix}/{document_id}/{timestamp}-{attachment_name}"
        s3_client.put_object(
            Bucket=bucket_name, Key=attachment_key, Body=attachment_bytes
        )
        result["attachment_key"] = attachment_key
    return result
