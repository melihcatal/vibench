import os
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError

from storage_client import get_storage_client
from storage_models import PresignedDownloadResponse


def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expiration: int = 3600,
) -> PresignedDownloadResponse:
    """
    Creates a time-limited signed download URL for an object in Amazon S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key of the object in the bucket.
        expiration: Time in seconds for the presigned URL to remain valid.

    Returns:
        PresignedDownloadResponse containing the presigned URL and expiration time.
    """
    s3_client = get_storage_client()

    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_key,
            },
            ExpiresIn=expiration,
        )

        expires_at = datetime.utcnow() + timedelta(seconds=expiration)

        return PresignedDownloadResponse(
            download_url=url, expires_at=expires_at, provider="aws_s3"
        )
    except ClientError as e:
        raise Exception(f"Failed to generate presigned URL: {e}")
