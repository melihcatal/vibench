import boto3
import os
from typing import Optional
from botocore.config import Config

# AWS S3 configuration
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
S3_ENDPOINT_URL = os.environ.get(
    "S3_ENDPOINT_URL"
)  # For custom endpoints (e.g., MinIO)

# S3 client configuration
S3_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "standard"}, connect_timeout=10, read_timeout=30
)

# Global S3 client instance
_s3_client = None


def get_s3_client():
    """
    Get or create an AWS S3 client with configuration from environment variables.

    Returns:
        boto3 S3 client instance
    """
    global _s3_client

    if _s3_client is None:
        client_kwargs = {"region_name": AWS_REGION, "config": S3_CONFIG}

        # Add credentials if provided
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            client_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
            client_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

            if AWS_SESSION_TOKEN:
                client_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

        # Add custom endpoint if provided
        if S3_ENDPOINT_URL:
            client_kwargs["endpoint_url"] = S3_ENDPOINT_URL

        _s3_client = boto3.client("s3", **client_kwargs)

    return _s3_client


def get_s3_resource():
    """
    Get or create an AWS S3 resource client.

    Returns:
        boto3 S3 resource instance
    """
    resource_kwargs = {"region_name": AWS_REGION}

    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        resource_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        resource_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

        if AWS_SESSION_TOKEN:
            resource_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

    if S3_ENDPOINT_URL:
        resource_kwargs["endpoint_url"] = S3_ENDPOINT_URL

    return boto3.resource("s3", **resource_kwargs)


def validate_bucket_name(bucket_name: str) -> bool:
    """
    Validate S3 bucket name according to AWS naming rules.

    Args:
        bucket_name: Bucket name to validate

    Returns:
        True if valid, False otherwise
    """
    if not bucket_name:
        return False

    # Length validation
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False

    # Character validation
    import re

    pattern = r"^[a-z0-9][a-z0-9.-]*[a-z0-9]$"
    if not re.match(pattern, bucket_name):
        return False

    # No consecutive periods or hyphens
    if ".." in bucket_name or ".-" in bucket_name or "-." in bucket_name:
        return False

    # Not an IP address
    ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if re.match(ip_pattern, bucket_name):
        return False

    return True


def get_object_url(bucket_name: str, object_key: str, region: str = None) -> str:
    """
    Generate the public URL for an S3 object.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path)
        region: AWS region (defaults to configured region)

    Returns:
        Public URL for the object
    """
    if region is None:
        region = AWS_REGION

    # Format: https://bucket-name.s3.region.amazonaws.com/key
    return f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"


def parse_s3_uri(s3_uri: str) -> tuple:
    """
    Parse an S3 URI (s3://bucket/key) into bucket and key.

    Args:
        s3_uri: S3 URI in format s3://bucket/key

    Returns:
        Tuple of (bucket_name, object_key)

    Raises:
        ValueError: If URI format is invalid
    """
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI: {s3_uri}. Must start with 's3://'")

    # Remove s3:// prefix
    path = s3_uri[5:]

    # Split into bucket and key
    parts = path.split("/", 1)
    bucket_name = parts[0]

    if len(parts) > 1:
        object_key = parts[1]
    else:
        object_key = ""

    return bucket_name, object_key


def create_s3_uri(bucket_name: str, object_key: str) -> str:
    """
    Create an S3 URI from bucket and key.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path)

    Returns:
        S3 URI in format s3://bucket/key
    """
    return f"s3://{bucket_name}/{object_key}"
