import os
import boto3
from storage_client import get_s3_client


def create_presigned_download_url(bucket_name, key, expiration_seconds=3600):
    """Create a time-limited pre‑signed URL for downloading an object from Amazon S3.

    Authenticates via AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY.
    """
    s3_client = get_s3_client()
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=expiration_seconds,
    )
