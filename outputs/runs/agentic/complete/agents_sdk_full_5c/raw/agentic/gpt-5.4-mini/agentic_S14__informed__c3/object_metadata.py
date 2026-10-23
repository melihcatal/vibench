from __future__ import annotations

from typing import Any

from storage_client import create_storage_client
from storage_models import ObjectRef, StoredObjectMetadata, normalize_mapping


def read_object_metadata(ref: ObjectRef) -> StoredObjectMetadata:
    s3 = create_storage_client("s3")
    kwargs: dict[str, Any] = {"Bucket": ref.bucket, "Key": ref.key}
    if ref.version_id:
        kwargs["VersionId"] = ref.version_id
    response = s3.head_object(**kwargs)
    return StoredObjectMetadata(
        bucket=ref.bucket,
        key=ref.key,
        etag=response.get("ETag"),
        size=response.get("ContentLength"),
        last_modified=str(response.get("LastModified")) if response.get("LastModified") else None,
        content_type=response.get("ContentType"),
        metadata=normalize_mapping(response.get("Metadata")),
        raw=response,
    )
