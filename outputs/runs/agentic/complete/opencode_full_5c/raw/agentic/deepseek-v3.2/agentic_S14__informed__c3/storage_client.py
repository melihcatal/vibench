import boto3
import os
from typing import Optional


def get_s3_client():
    """
    Get an authenticated Amazon S3 client.

    Returns:
        boto3.client: Configured S3 client
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise EnvironmentError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )


def validate_bucket_name(bucket_name: str) -> bool:
    """
    Validate S3 bucket name format.

    Args:
        bucket_name: Bucket name to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not bucket_name:
        return False

    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False

    if not bucket_name[0].islower() or not bucket_name[-1].islower():
        return False

    if ".." in bucket_name or ".-" in bucket_name or "-." in bucket_name:
        return False

    return True


def normalize_object_key(object_key: str) -> str:
    """
    Normalize object key by removing leading/trailing slashes.

    Args:
        object_key: Object key to normalize

    Returns:
        str: Normalized object key
    """
    return object_key.strip("/")


def parse_s3_url(s3_url: str) -> tuple[str, str]:
    """
    Parse S3 URL into bucket and key.

    Args:
        s3_url: S3 URL in format s3://bucket/key

    Returns:
        tuple: (bucket_name, object_key)
    """
    if not s3_url.startswith("s3://"):
        raise ValueError("Invalid S3 URL format. Must start with 's3://'")

    parts = s3_url[5:].split("/", 1)
    bucket_name = parts[0]
    object_key = parts[1] if len(parts) > 1 else ""

    return bucket_name, object_key
