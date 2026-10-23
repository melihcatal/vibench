import base64
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


@dataclass
class ArchiveResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    sha256: str
    archived_at: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_payload(payload: Any) -> bytes:
    if payload is None:
        return b""
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        try:
            decoded = base64.b64decode(payload, validate=True)
            if base64.b64encode(decoded).decode("ascii").rstrip("=") == payload.rstrip("="):
                return decoded
        except Exception:
            pass
        return payload.encode("utf-8")
    if isinstance(payload, (dict, list)):
        return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return str(payload).encode("utf-8")


def _archive_key(record: Dict[str, Any], source_name: str) -> str:
    record_id = str(record.get("id") or record.get("document_id") or record.get("record_id") or "unknown")
    timestamp = record.get("updated_at") or record.get("created_at") or _utc_now_iso()
    safe_timestamp = str(timestamp).replace(":", "-")
    digest = hashlib.sha256(_normalize_payload(record).hex().encode("utf-8")).hexdigest()[:16]
    return f"archives/{record_id}/{safe_timestamp}-{source_name}-{digest}.json"


def archive_record_export(record: Dict[str, Any], source_name: str, bucket: Optional[str] = None, prefix: str = "") -> ArchiveResult:
    bucket_name = bucket or os.environ.get("AWS_S3_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("AWS_S3_ARCHIVE_BUCKET is required")
    s3 = boto3.client("s3")
    archived_at = _utc_now_iso()
    body = json.dumps(
        {"archived_at": archived_at, "source_name": source_name, "record": record},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    sha256 = hashlib.sha256(body).hexdigest()
    key = prefix.rstrip("/") + "/" + _archive_key(record, source_name) if prefix else _archive_key(record, source_name)
    try:
        response = s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=body,
            ContentType="application/json",
            Metadata={"sha256": sha256, "source_name": source_name},
        )
    except ClientError as exc:
        raise RuntimeError(f"Failed to archive record export to Amazon S3: {exc}") from exc
    return ArchiveResult(
        bucket=bucket_name,
        key=key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        sha256=sha256,
        archived_at=archived_at,
    )


def archive_attachment_bytes(data: bytes, attachment_name: str, bucket: Optional[str] = None, prefix: str = "attachments") -> ArchiveResult:
    bucket_name = bucket or os.environ.get("AWS_S3_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("AWS_S3_ARCHIVE_BUCKET is required")
    s3 = boto3.client("s3")
    archived_at = _utc_now_iso()
    sha256 = hashlib.sha256(data).hexdigest()
    key = f"{prefix.rstrip('/')}/{attachment_name}-{sha256[:16]}"
    try:
        response = s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=data,
            ContentType="application/octet-stream",
            Metadata={"sha256": sha256, "attachment_name": attachment_name},
        )
    except ClientError as exc:
        raise RuntimeError(f"Failed to archive attachment to Amazon S3: {exc}") from exc
    return ArchiveResult(
        bucket=bucket_name,
        key=key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        sha256=sha256,
        archived_at=archived_at,
    )
