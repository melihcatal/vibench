# presigned_download.py
# [SAME-SCENARIO] Creates time-limited signed download URL for an object (Amazon S3 example)

import os
import boto3
from botocore.client import Config
from storage_client import create_s3_client


# Configuration - expects AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars
def generate_presigned_url(
    bucket: str, key: str, expires_in_seconds: int = 3600
) -> str:
    """Generates a presigned URL to retrieve an S3 object.
    Args:
        bucket (str): Bucket name.
        key (str): Object key/path.
        expires_in_seconds (int): URL expiration time in seconds (default: 1 hour).
    Returns:
        str: Signed URL.
    """
    s3 = create_s3_client()
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in_seconds,
    )
    return url


# Example usage (uncomment to test)
# url = generate_presigned_url('my-bucket', 'example.txt', expires_in_seconds=1800)
# print('Download URL:', url)
