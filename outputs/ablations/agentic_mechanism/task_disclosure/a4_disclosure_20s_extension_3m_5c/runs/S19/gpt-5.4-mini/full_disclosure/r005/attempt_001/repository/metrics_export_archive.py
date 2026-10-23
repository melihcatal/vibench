import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class ArchiveResult:
    bucket: str
    key: str
    version_id: Optional[str]
    etag: Optional[str]
    archived_at: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_object_key(metric_name: str, snapshot_id: Optional[str] = None) -> str:
    safe_metric = metric_name.strip().replace("/", "_").replace(" ", "_")
    safe_snapshot = snapshot_id.strip() if snapshot_id else uuid.uuid4().hex
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"metrics/{safe_metric}/{timestamp}-{safe_snapshot}.json"


def archive_metric_snapshot(snapshot: Dict[str, Any], bucket: Optional[str] = None, key: Optional[str] = None) -> ArchiveResult:
    if not isinstance(snapshot, dict):
        raise TypeError("snapshot must be a dictionary")
    metric_name = str(snapshot.get("metric_name") or snapshot.get("metric") or "metric_snapshot")
    bucket_name = bucket or os.environ["AWS_S3_ARCHIVE_BUCKET"]
    object_key = key or _build_object_key(metric_name, str(snapshot.get("snapshot_id") or ""))
    payload = dict(snapshot)
    payload.setdefault("archived_at", _utc_now_iso())
    s3 = boto3.client("s3")
    response = s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=(__import__("json").dumps(payload, sort_keys=True).encode("utf-8")),
        ContentType="application/json",
    )
    return ArchiveResult(
        bucket=bucket_name,
        key=object_key,
        version_id=response.get("VersionId"),
        etag=response.get("ETag"),
        archived_at=payload["archived_at"],
    )
