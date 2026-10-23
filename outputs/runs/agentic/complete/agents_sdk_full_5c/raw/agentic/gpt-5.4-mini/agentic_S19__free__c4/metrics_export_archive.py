from __future__ import annotations

from google.cloud import storage

from observability_client import load_config, storage_client
from observability_models import ArchiveResult


def metrics_export_archive(blob_name: str, payload: bytes) -> dict:
    config = load_config()
    if not config.storage_bucket:
        raise ValueError("METRICS_EXPORT_BUCKET is required")
    client: storage.Client = storage_client()
    bucket = client.bucket(config.storage_bucket)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(payload, content_type="application/octet-stream")
    result = ArchiveResult(bucket=config.storage_bucket, object_name=blob_name, size=len(payload))
    return result.__dict__
