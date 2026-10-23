from __future__ import annotations

from typing import Any, Dict

from storage_client import get_s3_client, load_storage_config
from storage_models import ObjectMetadata


def read_object_metadata(bucket: str, key: str) -> Dict[str, Any]:
    config = load_storage_config(bucket)
    client = get_s3_client(config)
    response = client.head_object(Bucket=bucket, Key=key)
    metadata = ObjectMetadata(
        bucket=bucket,
        key=key,
        etag=response.get("ETag"),
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        last_modified=str(response.get("LastModified")) if response.get("LastModified") else None,
        metadata=response.get("Metadata"),
    )
    return {
        "bucket": metadata.bucket,
        "key": metadata.key,
        "etag": metadata.etag,
        "content_length": metadata.content_length,
        "content_type": metadata.content_type,
        "last_modified": metadata.last_modified,
        "metadata": metadata.metadata or {},
    }
