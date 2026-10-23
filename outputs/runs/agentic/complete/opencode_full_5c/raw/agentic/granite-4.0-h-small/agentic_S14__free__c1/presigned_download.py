# presigned_download.py
# [SAME-SCENARIO] create a time-limited signed download URL
# Using AWS S3 as the concrete managed object storage provider
import boto3
from typing import Optional, Tuple

# Load configuration from local helper
from storage_client import get_s3_client, get_bucket_name


def generate_presigned_url(object_key: str, expires_in_seconds: int = 3600) -> str:
    """Generate a pre-signed URL to download an object from S3.

    Args:
        object_key: The key (path) of the object in the bucket.
        expires_in_seconds: Expiration time in seconds (default 1 hour).

    Returns:
        A URL string that can be used for direct download.
    """
    s3 = get_s3_client()
    try:
        bucket = get_bucket_name()
    except Exception:
        # Fallback to an environment variable if bucket name not configured locally
        bucket = boto3.client("s3").meta.client.get_bucket_location(Bucket="")
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": object_key},
        ExpiresIn=expires_in_seconds,
    )
    return url
