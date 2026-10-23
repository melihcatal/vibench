from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


DEFAULT_AWS_REGION = "us-east-1"
DEFAULT_S3_PREFIX = "metric-snapshots"
DEFAULT_S3_STORAGE_CLASS = "STANDARD_IA"


def _to_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("empty datetime value")
        text = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    raise TypeError(f"Cannot convert {type(value).__name__} to datetime")


def _sanitize_component(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "-" for ch in value.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-_.") or "snapshot"


def _read_bytes(source: str | Path | bytes) -> bytes:
    if isinstance(source, bytes):
        return source
    path = Path(source)
    return path.read_bytes()


def _coerce_metadata(metadata: Optional[Mapping[str, Any]]) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(key): str(value) for key, value in metadata.items()}


@dataclass(frozen=True)
class ExportArchiveResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    checksum_sha256: str
    size_bytes: int
    archived_at: datetime


class MetricsExportArchiver:
    def __init__(self, bucket: str, region_name: str = DEFAULT_AWS_REGION, s3_client: Any | None = None) -> None:
        self.bucket = bucket
        self.region_name = region_name
        self._s3 = s3_client or boto3.client("s3", region_name=region_name)

    def archive_export(
        self,
        export_source: str | Path | bytes,
        metric_name: str,
        *,
        archived_at: datetime | str | int | float | None = None,
        snapshot_id: Optional[str] = None,
        prefix: str = DEFAULT_S3_PREFIX,
        metadata: Optional[Mapping[str, Any]] = None,
        content_type: Optional[str] = None,
        storage_class: str = DEFAULT_S3_STORAGE_CLASS,
    ) -> ExportArchiveResult:
        payload = _read_bytes(export_source)
        checksum = hashlib.sha256(payload).hexdigest()
        archived_dt = _to_datetime(archived_at or datetime.now(timezone.utc))
        stamp = archived_dt.strftime("%Y%m%dT%H%M%SZ")
        metric_slug = _sanitize_component(metric_name)
        snapshot_slug = _sanitize_component(snapshot_id or checksum[:12])
        key = f"{prefix.strip('/')}/{metric_slug}/{stamp}-{snapshot_slug}.json"
        extra_args: dict[str, Any] = {
            "Metadata": {
                **_coerce_metadata(metadata),
                "metric-name": metric_name,
                "checksum-sha256": checksum,
            },
            "StorageClass": storage_class,
        }
        if content_type:
            extra_args["ContentType"] = content_type
        else:
            guessed, _ = mimetypes.guess_type(key)
            extra_args["ContentType"] = guessed or "application/json"
        extra_args["ContentSHA256"] = base64.b64encode(hashlib.sha256(payload).digest()).decode("ascii")
        try:
            response = self._s3.put_object(Bucket=self.bucket, Key=key, Body=payload, **extra_args)
        except (ClientError, BotoCoreError) as exc:
            raise RuntimeError(f"Failed to archive metric export to s3://{self.bucket}/{key}") from exc
        return ExportArchiveResult(
            bucket=self.bucket,
            key=key,
            etag=response.get("ETag"),
            version_id=response.get("VersionId"),
            checksum_sha256=checksum,
            size_bytes=len(payload),
            archived_at=archived_dt,
        )


def archive_metric_export(
    export_source: str | Path | bytes,
    metric_name: str,
    bucket: str,
    *,
    region_name: str = DEFAULT_AWS_REGION,
    archived_at: datetime | str | int | float | None = None,
    snapshot_id: Optional[str] = None,
    prefix: str = DEFAULT_S3_PREFIX,
    metadata: Optional[Mapping[str, Any]] = None,
    content_type: Optional[str] = None,
    storage_class: str = DEFAULT_S3_STORAGE_CLASS,
) -> ExportArchiveResult:
    archiver = MetricsExportArchiver(bucket=bucket, region_name=region_name)
    return archiver.archive_export(
        export_source,
        metric_name,
        archived_at=archived_at,
        snapshot_id=snapshot_id,
        prefix=prefix,
        metadata=metadata,
        content_type=content_type,
        storage_class=storage_class,
    )
