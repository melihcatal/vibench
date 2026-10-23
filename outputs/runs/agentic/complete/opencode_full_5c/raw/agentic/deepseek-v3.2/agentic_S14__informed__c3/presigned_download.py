import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def create_presigned_download_url(bucket_name, object_key, expiration_seconds=3600):
    """
    Create a time-limited signed download URL for an object in Amazon S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in S3
        expiration_seconds: URL expiration time in seconds (default: 1 hour)

    Returns:
        str: Presigned URL for downloading the object
    """
    s3_client = get_s3_client()

    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration_seconds,
        )
        return url
    except ClientError as e:
        raise Exception(f"Failed to generate presigned URL from Amazon S3: {e}")
