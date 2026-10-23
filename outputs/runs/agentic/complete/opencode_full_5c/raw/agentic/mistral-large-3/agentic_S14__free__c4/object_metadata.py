from typing import Dict

from storage_client import (
    get_storage_client,
    normalize_bucket_name,
    normalize_object_key,
)
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def object_metadata(bucket: str, key: str) -> ObjectMetadataResponse:
    """
    Reads object metadata or head information from Amazon S3.

    Args:
        bucket: Name of the S3 bucket.
        key: Object key (path) in the bucket.

    Returns:
        ObjectMetadataResponse: Contains metadata and head information about the object.
    """
    client = get_storage_client()
    bucket = normalize_bucket_name(bucket)
    key = normalize_object_key(key)

    try:
        response = client.head_object(Bucket=bucket, Key=key)
        return ObjectMetadataResponse(
            bucket=bucket,
            key=key,
            content_type=response.get("ContentType"),
            content_length=response["ContentLength"],
            etag=response["ETag"].strip('"'),
            last_modified=response["LastModified"].isoformat(),
            metadata=response.get("Metadata", {}),
            version_id=response.get("VersionId"),
        )
    except Exception as e:
        raise Exception(f"Failed to fetch metadata for S3 object: {e}")
