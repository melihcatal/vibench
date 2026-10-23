from typing import Dict, Optional

from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadata


def get_object_metadata(key: str) -> ObjectMetadata:
    """
    Retrieve metadata for an object stored in Amazon S3.
    """
    client = get_storage_client()
    bucket = get_bucket_name()

    response = client.head_object(Bucket=bucket, Key=key)

    return ObjectMetadata(
        key=key,
        size=response["ContentLength"],
        etag=response["ETag"].strip('"'),
        last_modified=response["LastModified"].isoformat(),
        storage_class=response["StorageClass"],
        content_type=response.get("ContentType"),
        metadata=response.get("Metadata"),
    )