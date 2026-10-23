import base64
import hashlib
import mimetypes
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO, Optional

import boto3
from botocore.client import Config


@dataclass
class ArchiveResult:
    bucket: str
    key: str
    etag: str
    version_id: Optional[str]
    sha256: str
    size_bytes: int


def _s3_client():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("s3", region_name=region, config=Config(signature_version="s3v4"))


def _normalize_prefix(prefix: str) -> str:
    prefix = prefix.strip("/")
    return f"{prefix}/" if prefix else ""


def _build_key(source_name: str, prefix: str = "record-export-archive") -> str:
    stem = Path(source_name).stem or "export"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    digest = hashlib.sha256(f"{source_name}:{timestamp}".encode("utf-8")).hexdigest()[:16]
    return f"{_normalize_prefix(prefix)}{stem}/{timestamp}-{digest}{Path(source_name).suffix}"


def _sha256_and_size(data: BinaryIO) -> tuple[str, int, bytes]:
    hasher = hashlib.sha256()
    chunks = []
    size = 0
    while True:
        chunk = data.read(1024 * 1024)
        if not chunk:
            break
        if isinstance(chunk, str):
            chunk = chunk.encode("utf-8")
        chunks.append(chunk)
        hasher.update(chunk)
        size += len(chunk)
    return hasher.hexdigest(), size, b"".join(chunks)


def archive_export(
    source_path: str,
    *,
    bucket: Optional[str] = None,
    key_prefix: str = "record-export-archive",
    content_type: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> ArchiveResult:
    bucket = bucket or os.environ.get("RECORD_EXPORT_ARCHIVE_BUCKET")
    if not bucket:
        raise ValueError("bucket is required via argument or RECORD_EXPORT_ARCHIVE_BUCKET")

    path = Path(source_path)
    if not path.is_file():
        raise FileNotFoundError(source_path)

    detected_content_type, _ = mimetypes.guess_type(path.name)
    final_content_type = content_type or detected_content_type or "application/octet-stream"

    with path.open("rb") as fh:
        sha256, size_bytes, payload = _sha256_and_size(fh)

    key = _build_key(path.name, key_prefix)
    client = _s3_client()
    extra_args: dict[str, Any] = {
        "Bucket": bucket,
        "Key": key,
        "Body": payload,
        "ContentType": final_content_type,
        "Metadata": {**(metadata or {}), "sha256": sha256, "source-filename": path.name},
    }
    response = client.put_object(**extra_args)
    return ArchiveResult(
        bucket=bucket,
        key=key,
        etag=str(response.get("ETag", "")).strip('"'),
        version_id=response.get("VersionId"),
        sha256=sha256,
        size_bytes=size_bytes,
    )


def archive_export_bytes(
    payload: bytes,
    filename: str,
    *,
    bucket: Optional[str] = None,
    key_prefix: str = "record-export-archive",
    content_type: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> ArchiveResult:
    bucket = bucket or os.environ.get("RECORD_EXPORT_ARCHIVE_BUCKET")
    if not bucket:
        raise ValueError("bucket is required via argument or RECORD_EXPORT_ARCHIVE_BUCKET")

    sha256 = hashlib.sha256(payload).hexdigest()
    key = _build_key(filename, key_prefix)
    detected_content_type, _ = mimetypes.guess_type(filename)
    final_content_type = content_type or detected_content_type or "application/octet-stream"
    client = _s3_client()
    response = client.put_object(
        Bucket=bucket,
        Key=key,
        Body=payload,
        ContentType=final_content_type,
        Metadata={**(metadata or {}), "sha256": sha256, "source-filename": filename},
    )
    return ArchiveResult(
        bucket=bucket,
        key=key,
        etag=str(response.get("ETag", "")).strip('"'),
        version_id=response.get("VersionId"),
        sha256=sha256,
        size_bytes=len(payload),
    )


def archive_export_base64(
    encoded_payload: str,
    filename: str,
    *,
    bucket: Optional[str] = None,
    key_prefix: str = "record-export-archive",
    content_type: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> ArchiveResult:
    return archive_export_bytes(
        base64.b64decode(encoded_payload),
        filename,
        bucket=bucket,
        key_prefix=key_prefix,
        content_type=content_type,
        metadata=metadata,
    )
