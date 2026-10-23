from __future__ import annotations

import json
from datetime import datetime, timezone

from observability_client import load_config, storage_client
from observability_models import ArchiveResult


def metrics_export_archive(snapshot: dict, object_name: str | None = None) -> ArchiveResult:
    cfg = load_config()
    if not cfg.storage_bucket:
        raise ValueError("METRICS_ARCHIVE_BUCKET must be set")
    client = storage_client()
    bucket = client.bucket(cfg.storage_bucket)
    final_name = object_name or f"metrics/{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    blob = bucket.blob(final_name)
    payload = json.dumps(snapshot, sort_keys=True).encode("utf-8")
    blob.upload_from_string(payload, content_type="application/json")
    return ArchiveResult(bucket=cfg.storage_bucket, object_name=final_name, bytes_written=len(payload))
