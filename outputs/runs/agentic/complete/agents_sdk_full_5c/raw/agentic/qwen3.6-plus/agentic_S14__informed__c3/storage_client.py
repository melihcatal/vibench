"""
Local configuration and client helper utilities for Amazon S3 Managed Object Storage.
"""

import os
import boto3
from botocore.config import Config


def get_s3_client(region_name: str = None) -> boto3.client:
    """
    Create and return a configured boto3 S3 client using AWS credentials from environment.

    Environment variables used:
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY
        AWS_DEFAULT_REGION (optional, overridden by region_name parameter)

    Returns:
        boto3.client: Configured S3 client instance.
    """
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    config = Config(
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
        s3={"addressing_style": "path"},
    )

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    client = session.client("s3", config=config)
    return client


def validate_bucket_name(bucket_name: str) -> bool:
    """
    Validate an S3 bucket name against AWS naming rules.

    Args:
        bucket_name: The S3 bucket name to validate.

    Returns:
        bool: True if valid, raises ValueError otherwise.
    """
    if not bucket_name:
        raise ValueError("Bucket name cannot be empty")
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        raise ValueError("Bucket name must be between 3 and 63 characters")
    if not bucket_name[0].isalnum() or not bucket_name[-1].isalnum():
        raise ValueError("Bucket name must start and end with a letter or number")
    if ".." in bucket_name:
        raise ValueError("Bucket name cannot contain consecutive periods")
    return True


def build_object_key(prefix: str, filename: str) -> str:
    """
    Build a normalized S3 object key from prefix and filename.

    Args:
        prefix: The S3 prefix (folder path).
        filename: The object filename.

    Returns:
        str: Normalized object key with proper path separators.
    """
    prefix = prefix.strip("/")
    filename = filename.lstrip("/")
    if prefix:
        return f"{prefix}/{filename}"
    return filename
