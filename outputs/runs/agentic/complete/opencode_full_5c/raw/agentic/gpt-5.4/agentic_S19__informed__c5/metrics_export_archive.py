from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from typing import Any

from observability_client import current_timestamp_key, dumps_json, s3_client
from observability_models import ArchiveResponse


def _to_serializable(payload: Any) -> Any:
    if is_dataclass(payload):
        return asdict(payload)
    if isinstance(payload, list):
        return [_to_serializable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): _to_serializable(value) for key, value in payload.items()}
    return payload


def metrics_export_archive(
    bucket: str, metric_name: str, snapshot: Any, prefix: str = "metric-exports"
) -> ArchiveResponse:
    client = s3_client()
    exported_at = datetime.now(timezone.utc)
    object_key = current_timestamp_key(
        prefix=prefix, metric_name=metric_name, exported_at=exported_at
    )
    body = dumps_json(
        {
            "metric_name": metric_name,
            "exported_at": exported_at.isoformat(),
            "snapshot": _to_serializable(snapshot),
        }
    )
    response = client.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=body.encode("utf-8"),
        ContentType="application/json",
    )
    return ArchiveResponse(
        bucket=bucket,
        object_key=object_key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
    )
