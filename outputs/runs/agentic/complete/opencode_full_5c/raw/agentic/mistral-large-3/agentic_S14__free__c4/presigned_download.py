import os

from storage_client import (
    get_storage_client,
    normalize_bucket_name,
    normalize_object_key,
)
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def presigned_download(
    bucket: str, key: str, expires_in: int = 3600
) -> PresignedDownloadResponse:
    """
    Creates a time-limited signed download URL for an object in Amazon S3.

    Args:
        bucket: Name of the S3 bucket.
        key: Object key (path) in the bucket.
        expires_in: Time in seconds until the URL expires (default: 3600).

    Returns:
        PresignedDownloadResponse: Contains the presigned URL.
    """
    client = get_storage_client()
    bucket = normalize_bucket_name(bucket)
    key = normalize_object_key(key)

    try:
        url = client.generate_presigned_url(
            "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires_in
        )
        return PresignedDownloadResponse(url=url)
    except Exception as e:
        raise Exception(f"Failed to generate presigned URL for S3 object: {e}")
