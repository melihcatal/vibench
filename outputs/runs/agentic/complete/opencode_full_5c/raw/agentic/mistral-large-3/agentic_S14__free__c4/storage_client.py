import os
from typing import BinaryIO, Union

import boto3
from botocore.exceptions import ClientError

from storage_models import UploadRequest, UploadResponse


def get_storage_client():
    """
    Creates and returns an S3 client using AWS credentials from environment variables.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )


def normalize_bucket_name(bucket: str) -> str:
    """
    Normalizes the bucket name to ensure consistency.
    """
    return bucket.strip().lower()


def normalize_object_key(key: str) -> str:
    """
    Normalizes the object key to remove leading/trailing slashes and ensure consistency.
    """
    return key.strip("/")
