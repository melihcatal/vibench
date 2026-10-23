import base64
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ArchiveResult:
    bucket: str
    key: str
    etag: Optional[str]
    sha256: str


def _default_bucket() -> str:
    bucket = os.environ.get("AWS_S3_BUCKET") or os.environ.get("METRICS_EXPORT_BUCKET")
    if not bucket:
        raise ValueError("AWS_S3_BUCKET or METRICS_EXPORT_BUCKET is required")
    return bucket


def _s3_client():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if region:
        return boto3.client("s3", region_name=region)
    return boto3.client("s3")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _normalize_payload(snapshot: Any) -> bytes:
    if isinstance(snapshot, bytes):
        return snapshot
    if isinstance(snapshot, str):
        path = Path(snapshot)
        if path.exists() and path.is_file():
            return path.read_bytes()
        return snapshot.encode("utf-8")
    return json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")


def archive_metric_snapshot(snapshot: Any, metric_name: str, *, bucket: Optional[str] = None, prefix: str = "metrics-archives") -> ArchiveResult:
    payload = _normalize_payload(snapshot)
    digest = _sha256_bytes(payload)
    timestamp = datetime.now(timezone.utc).strftime("%Y/%m/%d/%H%M%S")
    key = f"{prefix}/{metric_name}/{timestamp}-{digest[:16]}.json"
    s3 = _s3_client()
    target_bucket = bucket or _default_bucket()
    try:
        response = s3.put_object(
            Bucket=target_bucket,
            Key=key,
            Body=payload,
            ContentType="application/json",
            Metadata={"sha256": digest, "metric-name": metric_name},
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"failed to archive metric snapshot to s3://{target_bucket}/{key}") from exc
    return ArchiveResult(bucket=target_bucket, key=key, etag=response.get("ETag"), sha256=digest)


def archive_metric_snapshot_from_base64(snapshot_b64: str, metric_name: str, *, bucket: Optional[str] = None, prefix: str = "metrics-archives") -> ArchiveResult:
    return archive_metric_snapshot(base64.b64decode(snapshot_b64), metric_name, bucket=bucket, prefix=prefix)


def archive_metric_snapshot_from_file(path: str, metric_name: str, *, bucket: Optional[str] = None, prefix: str = "metrics-archives") -> ArchiveResult:
    return archive_metric_snapshot(Path(path).read_bytes(), metric_name, bucket=bucket, prefix=prefix)
