import os
from typing import BinaryIO, Union

from storage_client import (
    get_storage_client,
    normalize_bucket_name,
    normalize_object_key,
)
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket: str,
    key: str,
    body: Union[bytes, BinaryIO],
    content_type: str = None,
    metadata: dict = None,
) -> UploadResponse:
    """
    Uploads a file or byte stream to Amazon S3 object storage.

    Args:
        bucket: Name of the S3 bucket.
        key: Object key (path) in the bucket.
        body: File-like object or bytes to upload.
        content_type: Optional MIME type of the object.
        metadata: Optional metadata dictionary for the object.

    Returns:
        UploadResponse: Contains bucket, key, etag, and version_id (if applicable).
    """
    client = get_storage_client()
    bucket = normalize_bucket_name(bucket)
    key = normalize_object_key(key)

    try:
        response = client.put_object(
            Bucket=bucket,
            Key=key,
            Body=body,
            ContentType=content_type,
            Metadata=metadata or {},
        )
        return UploadResponse(
            bucket=bucket,
            key=key,
            etag=response["ETag"].strip('"'),
            version_id=response.get("VersionId"),
        )
    except ClientError as e:
        raise Exception(f"Failed to upload object to S3: {e}")
