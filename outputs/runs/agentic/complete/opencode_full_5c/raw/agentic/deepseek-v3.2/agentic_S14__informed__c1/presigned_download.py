import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def create_presigned_download_url(
    bucket_name: str, object_key: str, expiration: int = 3600
) -> str:
    """
    Create a time-limited signed download URL for an S3 object.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in S3
        expiration: URL expiration time in seconds (default: 1 hour)

    Returns:
        Presigned URL for downloading the object
    """
    s3_client = get_s3_client()

    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return url
    except ClientError as e:
        raise Exception(f"Failed to generate presigned URL: {e}")
