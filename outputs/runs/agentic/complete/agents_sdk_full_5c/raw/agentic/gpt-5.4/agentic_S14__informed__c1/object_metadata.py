from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client
from storage_models import ObjectMetadata, normalize_metadata_map


def get_object_metadata(bucket: str, key: str, region_name: Optional[str] = None) -> ObjectMetadata:
    s3 = get_s3_client(region_name=region_name)
    response = s3.head_object(Bucket=bucket, Key=key)
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        etag=response.get("ETag"),
        size=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        last_modified=response.get("LastModified"),
        metadata=normalize_metadata_map(response.get("Metadata")),
        version_id=response.get("VersionId"),
        storage_class=response.get("StorageClass"),
    )
