import boto3
import os
from typing import Optional


def get_s3_client():
    """
    Get an authenticated S3 client using AWS credentials.

    Returns:
        boto3 S3 client
    """
    # Check for AWS credentials in environment
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found in environment. "
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )

    # Create S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    return s3_client


def validate_bucket_name(bucket_name: str) -> bool:
    """
    Validate S3 bucket name format.

    Args:
        bucket_name: Bucket name to validate

    Returns:
        True if valid, False otherwise
    """
    if not bucket_name:
        return False

    # Basic S3 bucket name validation
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False

    # Check for invalid characters
    import re

    pattern = r"^[a-z0-9][a-z0-9.-]*[a-z0-9]$"
    if not re.match(pattern, bucket_name):
        return False

    # Check for consecutive dots or hyphens
    if ".." in bucket_name or ".-" in bucket_name or "-." in bucket_name:
        return False

    return True


def parse_s3_uri(s3_uri: str) -> tuple:
    """
    Parse an S3 URI into bucket and key components.

    Args:
        s3_uri: S3 URI in format s3://bucket/key

    Returns:
        Tuple of (bucket_name, object_key)
    """
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI: {s3_uri}. Must start with 's3://'")

    # Remove s3:// prefix
    path = s3_uri[5:]

    # Split into bucket and key
    parts = path.split("/", 1)
    bucket_name = parts[0]
    object_key = parts[1] if len(parts) > 1 else ""

    return bucket_name, object_key


def build_s3_uri(bucket_name: str, object_key: str = "") -> str:
    """
    Build an S3 URI from bucket and key components.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (optional)

    Returns:
        S3 URI string
    """
    if object_key:
        return f"s3://{bucket_name}/{object_key}"
    else:
        return f"s3://{bucket_name}"
