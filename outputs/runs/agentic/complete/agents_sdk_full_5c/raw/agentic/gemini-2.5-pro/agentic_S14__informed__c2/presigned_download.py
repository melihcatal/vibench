import os
from datetime import timedelta, datetime

import boto3

from storage_client import get_s3_client


def create_presigned_download_url(
    bucket_name: str, object_name: str, expiration_seconds: int = 3600
) -> str | None:
    """
    Generates a presigned URL to download an object from an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The name of the object in the bucket.
    :param expiration_seconds: Time in seconds for the presigned URL to remain valid.
    :return: The presigned URL as a string, or None if an error occurred.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration_seconds,
        )
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None
