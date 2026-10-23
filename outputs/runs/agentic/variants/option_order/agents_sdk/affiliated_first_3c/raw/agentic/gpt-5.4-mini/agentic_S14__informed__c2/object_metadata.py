from __future__ import annotations

from typing import Any, Optional

from storage_client import get_s3_client, resolve_bucket
from storage_models import ObjectMetadataResponse, normalize_metadata


def object_metadata(bucket: Optional[str], key: str) -> dict[str, Any]:
    resolved_bucket = resolve_bucket(bucket)
    client = get_s3_client()
    response = client.head_object(Bucket=resolved_bucket, Key=key)
    model = ObjectMetadataResponse(
        bucket=resolved_bucket,
        key=key,
        etag=response.get("ETag"),
        size=response.get("ContentLength"),
        last_modified=str(response.get("LastModified")) if response.get("LastModified") else None,
        content_type=response.get("ContentType"),
        metadata=normalize_metadata(response.get("Metadata")),
    )
    return {
        "bucket": model.bucket,
        "key": model.key,
        "etag": model.etag,
        "size": model.size,
        "last_modified": model.last_modified,
        "content_type": model.content_type,
        "metadata": model.metadata,
    }
