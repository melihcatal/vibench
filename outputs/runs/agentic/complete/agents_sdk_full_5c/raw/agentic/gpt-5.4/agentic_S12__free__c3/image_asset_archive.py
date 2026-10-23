from __future__ import annotations

from typing import Any, Dict

from vision_client import GCS_ARCHIVE_BUCKET, dump_json, get_storage_client
from vision_models import ArchiveResult


def image_asset_archive(artifact_name: str, payload: Dict[str, Any], bucket_name: str = GCS_ARCHIVE_BUCKET) -> ArchiveResult:
    if not bucket_name:
        raise ValueError("GCS_ARCHIVE_BUCKET or bucket_name is required")
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(artifact_name)
    blob.upload_from_string(dump_json(payload), content_type="application/json")
    return ArchiveResult(
        bucket=bucket_name,
        object_name=artifact_name,
        uri=f"gs://{bucket_name}/{artifact_name}",
    )
