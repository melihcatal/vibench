# presigned_download.py
# Creates a time-limited signed download URL for a stored S3 object

import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def generate_presigned_url(
    bucket: str, key: str, expires_in_seconds: int = 3600
) -> str:
    """Generate a presigned URL to download an object."""
    client = get_s3_client()
    try:
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_in_seconds,
        )
    except ClientError as exc:
        raise RuntimeError(f"Presigned URL generation failed: {exc}") from exc
    return url


# Example usage:
# url = generate_presigned_url("my-bucket", "path/to/file.txt", expires_in_seconds=600)
# print(url)
