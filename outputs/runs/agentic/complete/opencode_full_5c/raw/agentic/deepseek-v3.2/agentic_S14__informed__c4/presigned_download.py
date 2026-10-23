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
        object_key: Object key (path) in the bucket
        expiration: URL expiration time in seconds (default: 1 hour)

    Returns:
        Presigned URL string or empty string on error
    """
    s3_client = get_s3_client()

    try:
        # Generate the presigned URL
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ""


def create_presigned_upload_url(
    bucket_name: str, object_key: str, expiration: int = 3600, content_type: str = None
) -> str:
    """
    Create a time-limited signed upload URL for S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in the bucket
        expiration: URL expiration time in seconds (default: 1 hour)
        content_type: Required content type for upload

    Returns:
        Presigned URL string or empty string on error
    """
    s3_client = get_s3_client()

    params = {"Bucket": bucket_name, "Key": object_key}

    if content_type:
        params["ContentType"] = content_type

    try:
        response = s3_client.generate_presigned_url(
            "put_object", Params=params, ExpiresIn=expiration
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned upload URL: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ""
