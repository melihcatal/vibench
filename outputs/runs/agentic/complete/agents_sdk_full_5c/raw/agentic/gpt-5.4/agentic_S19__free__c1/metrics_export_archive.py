from __future__ import annotations

import json
from typing import Any

from google.cloud import storage

from observability_client import config, storage_client
from observability_models import ExportArchiveResult


GCS_PROVIDER_HOST = "storage.googleapis.com"


def metrics_export_archive(snapshot: dict[str, Any], object_name: str, bucket: str | None = None) -> ExportArchiveResult:
    bucket_name = bucket or config.default_bucket
    if not bucket_name:
        raise ValueError("bucket must be provided or GCS_ARCHIVE_BUCKET must be set")
    client = storage_client()
    gcs_bucket = client.bucket(bucket_name)
    blob = gcs_bucket.blob(object_name)
    payload = json.dumps(snapshot, separators=(",", ":"), sort_keys=True).encode("utf-8")
    blob.upload_from_string(payload, content_type="application/json")
    blob.reload()
    return ExportArchiveResult(
        bucket=bucket_name,
        object_name=object_name,
        generation=getattr(blob, "generation", None),
        content_type=blob.content_type or "application/json",
        size_bytes=int(blob.size or len(payload)),
    )
