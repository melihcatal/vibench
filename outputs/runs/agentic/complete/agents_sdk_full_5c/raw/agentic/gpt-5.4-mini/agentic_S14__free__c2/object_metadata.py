from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, load_storage_config
from storage_models import MetadataResult


def object_metadata(bucket: Optional[str], key: str) -> MetadataResult:
    client = get_s3_client()
    resolved_bucket = bucket or load_storage_config().bucket
    if not resolved_bucket:
        raise ValueError("bucket is required")

    response = client.head_object(Bucket=resolved_bucket, Key=key)
    return MetadataResult(
        bucket=resolved_bucket,
        key=key,
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=response.get("ETag"),
        last_modified=response.get("LastModified").isoformat() if response.get("LastModified") else None,
        metadata=response.get("Metadata", {}),
    )
