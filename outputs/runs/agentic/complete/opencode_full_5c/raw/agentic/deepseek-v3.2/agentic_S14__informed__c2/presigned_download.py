import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def create_presigned_download_url(bucket_name, object_key, expiration_seconds=3600):
    """
    Create a time-limited signed download URL for an S3 object.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key
        expiration_seconds: URL expiration time in seconds (default 1 hour)

    Returns:
        dict: Result with signed URL or error
    """
    s3_client = get_s3_client()

    try:
        # Generate presigned URL
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration_seconds,
        )

        return {
            "success": True,
            "url": url,
            "bucket": bucket_name,
            "key": object_key,
            "expires_in_seconds": expiration_seconds,
            "provider": "Amazon S3",
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "provider": "Amazon S3"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "Amazon S3"}
