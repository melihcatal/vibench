import boto3
import os
from typing import Optional
from botocore.config import Config


def get_s3_client():
    """Initialize and return an AWS S3 client with configuration from environment."""
    # AWS configuration from environment variables
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    aws_endpoint_url = os.environ.get("AWS_S3_ENDPOINT_URL")

    # Configure client with appropriate settings
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=10,
        read_timeout=30,
    )

    # Create S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
        endpoint_url=aws_endpoint_url,
        config=config,
    )

    return s3_client


def validate_bucket_name(bucket_name: str) -> bool:
    """Validate S3 bucket name according to AWS rules."""
    if not bucket_name:
        return False

    # Basic validation
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False

    # Check for invalid characters
    import re

    pattern = r"^[a-z0-9][a-z0-9.-]*[a-z0-9]$"
    if not re.match(pattern, bucket_name):
        return False

    # Check for consecutive periods or hyphens
    if ".." in bucket_name or ".-" in bucket_name or "-." in bucket_name:
        return False

    # Check for IP address format
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", bucket_name):
        return False

    return True


def get_object_url(bucket: str, object_key: str, region: str = None) -> str:
    """Generate the public URL for an S3 object."""
    if not region:
        region = os.environ.get("AWS_REGION", "us-east-1")

    # Handle different region formats
    if region == "us-east-1":
        # us-east-1 doesn't include region in URL
        return f"https://{bucket}.s3.amazonaws.com/{object_key}"
    else:
        return f"https://{bucket}.s3.{region}.amazonaws.com/{object_key}"
