import boto3
import os
from typing import Optional


def get_s3_client():
    """
    Returns a configured AWS S3 client using environment variables.
    """
    # Get AWS credentials from environment
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    # Create S3 client
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    return session.client("s3")


def get_default_bucket() -> Optional[str]:
    """
    Returns the default S3 bucket from environment variable.
    """
    return os.getenv("AWS_S3_BUCKET")


def validate_bucket_name(bucket: str) -> bool:
    """
    Validates S3 bucket name according to AWS naming rules.
    """
    if not bucket:
        return False

    # Basic S3 bucket name validation
    if len(bucket) < 3 or len(bucket) > 63:
        return False

    # Check for invalid characters
    import re

    pattern = r"^[a-z0-9][a-z0-9.-]*[a-z0-9]$"
    if not re.match(pattern, bucket):
        return False

    # Check for consecutive dots
    if ".." in bucket:
        return False

    # Check for IP address format
    ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if re.match(ip_pattern, bucket):
        return False

    return True


def format_s3_url(bucket: str, key: str) -> str:
    """
    Formats a standard S3 URL for an object.
    """
    return f"s3://{bucket}/{key}"
