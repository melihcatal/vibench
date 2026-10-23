from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _to_utc_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
    else:
        raise TypeError(f"Unsupported datetime value: {type(value)!r}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True)
class MetricExportArchiveRequest:
    snapshot_id: str
    metric_name: str
    export_payload: Mapping[str, Any]
    archived_at: datetime
    bucket: Optional[str] = None
    object_key: Optional[str] = None
    content_type: str = "application/json"

    def __post_init__(self) -> None:
        object.__setattr__(self, "archived_at", _to_utc_datetime(self.archived_at))


@dataclass(frozen=True)
class MetricExportArchiveResult:
    snapshot_id: str
    metric_name: str
    archived_at: datetime
    bucket: str
    object_key: str
    object_uri: str


def _default_bucket() -> str:
    return _env("AWS_METRICS_ARCHIVE_BUCKET")


def _build_object_key(request: MetricExportArchiveRequest) -> str:
    safe_metric = request.metric_name.strip().replace("/", "_")
    ts = request.archived_at.strftime("%Y/%m/%d/%H%M%S")
    return request.object_key or f"metric-archives/{safe_metric}/{request.snapshot_id}/{ts}.json"


def archive_metric_export(request: MetricExportArchiveRequest) -> MetricExportArchiveResult:
    bucket = request.bucket or _default_bucket()
    object_key = _build_object_key(request)
    client = boto3.client("s3")
    body = __import__("json").dumps(
        {
            "snapshot_id": request.snapshot_id,
            "metric_name": request.metric_name,
            "archived_at": request.archived_at.isoformat(),
            "export_payload": request.export_payload,
        },
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    try:
        client.put_object(
            Bucket=bucket,
            Key=object_key,
            Body=body,
            ContentType=request.content_type,
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Failed to archive metric export to s3://{bucket}/{object_key}") from exc
    return MetricExportArchiveResult(
        snapshot_id=request.snapshot_id,
        metric_name=request.metric_name,
        archived_at=request.archived_at,
        bucket=bucket,
        object_key=object_key,
        object_uri=f"s3://{bucket}/{object_key}",
    )


__all__ = [
    "MetricExportArchiveRequest",
    "MetricExportArchiveResult",
    "archive_metric_export",
]
