import base64
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


def _normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        normalized[str(key)] = json.dumps(value, sort_keys=True, separators=(",", ":")) if isinstance(value, (dict, list)) else str(value)
    return normalized


def _parse_payload(payload: Any) -> bytes:
    if payload is None:
        return b""
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, bytearray):
        return bytes(payload)
    if isinstance(payload, str):
        try:
            return base64.b64decode(payload, validate=True)
        except Exception:
            return payload.encode("utf-8")
    if isinstance(payload, (dict, list)):
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return str(payload).encode("utf-8")


@dataclass
class RecordExportArchiveResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    sha256: Optional[str] = None


def archive_exported_record(
    record: Dict[str, Any],
    *,
    bucket: Optional[str] = None,
    prefix: str = "document-archives/",
    s3_client: Any = None,
) -> RecordExportArchiveResult:
    bucket_name = bucket or os.environ.get("AWS_S3_ARCHIVE_BUCKET") or os.environ.get("ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("Missing S3 bucket; set AWS_S3_ARCHIVE_BUCKET or ARCHIVE_BUCKET")

    client = s3_client or boto3.client("s3")

    record_id = str(record.get("id") or record.get("record_id") or record.get("document_id") or record.get("key") or "unknown")
    export_type = str(record.get("type") or record.get("content_type") or "snapshot")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = record.get("payload", record.get("content", record))
    data = _parse_payload(payload)

    digest = hashlib.sha256(data).hexdigest()
    key = f"{prefix.rstrip('/')}/{export_type}/{record_id}/{timestamp}-{digest[:16]}.json"

    metadata = _normalize_metadata(record.get("metadata") if isinstance(record.get("metadata"), dict) else None)
    metadata.update({
        "record-id": record_id,
        "export-type": export_type,
        "sha256": digest,
    })

    response = client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=data,
        ContentType="application/json",
        Metadata=metadata,
    )

    return RecordExportArchiveResult(
        bucket=bucket_name,
        key=key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        sha256=digest,
    )


def archive_exported_attachment(
    attachment: Dict[str, Any],
    *,
    bucket: Optional[str] = None,
    prefix: str = "attachment-archives/",
    s3_client: Any = None,
) -> RecordExportArchiveResult:
    return archive_exported_record(attachment, bucket=bucket, prefix=prefix, s3_client=s3_client)
