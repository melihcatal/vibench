import hashlib
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class ArchiveResult:
    bucket: str
    key: str
    etag: Optional[str]
    sha256: str


def _s3_client():
    return boto3.client("s3")


def _archive_key(record_id: str, source_name: str, content_type: str) -> str:
    safe_source = source_name.replace("/", "_").replace("\\", "_").strip() or "export"
    ext = "bin"
    if content_type in {"application/pdf"}:
        ext = "pdf"
    elif content_type.startswith("text/"):
        ext = "txt"
    elif content_type in {"application/json"}:
        ext = "json"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"exports/{record_id}/{timestamp}-{safe_source}.{ext}"


def archive_exported_document_snapshot(
    *,
    record_id: str,
    data: bytes,
    source_name: str,
    content_type: str = "application/octet-stream",
    bucket: Optional[str] = None,
) -> ArchiveResult:
    target_bucket = bucket or os.environ["S3_ARCHIVE_BUCKET"]
    key = _archive_key(record_id, source_name, content_type)
    sha256 = hashlib.sha256(data).hexdigest()
    client = _s3_client()
    try:
        response = client.put_object(
            Bucket=target_bucket,
            Key=key,
            Body=data,
            ContentType=content_type,
            Metadata={
                "record-id": record_id,
                "source-name": source_name,
                "sha256": sha256,
            },
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"failed to archive export to s3://{target_bucket}/{key}") from exc
    return ArchiveResult(
        bucket=target_bucket,
        key=key,
        etag=response.get("ETag"),
        sha256=sha256,
    )


def archive_exported_attachment(
    *,
    record_id: str,
    file_path: str,
    bucket: Optional[str] = None,
    content_type: str = "application/octet-stream",
) -> ArchiveResult:
    with open(file_path, "rb") as f:
        return archive_exported_document_snapshot(
            record_id=record_id,
            data=f.read(),
            source_name=os.path.basename(file_path),
            content_type=content_type,
            bucket=bucket,
        )
