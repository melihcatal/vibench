import os
import boto3
from botocore.config import Config


def get_s3_client(region=None, endpoint_url=None):
    """Create and return an AWS S3 client using boto3.

    Uses AWS credentials from environment variables:
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY
        AWS_DEFAULT_REGION or AWS_REGION

    Args:
        region: Optional AWS region override.
        endpoint_url: Optional custom endpoint (e.g., for S3-compatible services).

    Returns:
        boto3 S3 client instance.
    """
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region or os.environ.get("AWS_DEFAULT_REGION") or os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        s3={"addressing_style": "path"},
    )

    client_kwargs = {"config": config}
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url

    return session.client("s3", **client_kwargs)


def get_textract_client(region=None):
    """Create and return an AWS Textract client for document analysis."""
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region or os.environ.get("AWS_DEFAULT_REGION") or os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    return session.client("textract", region_name=region)


def get_translate_client(region=None):
    """Create and return an AWS Translate client for text translation."""
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region or os.environ.get("AWS_DEFAULT_REGION") or os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    return session.client("translate", region_name=region)


def validate_bucket_name(bucket_name):
    """Validate AWS S3 bucket naming conventions."""
    if not bucket_name:
        raise ValueError("Bucket name is required")
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        raise ValueError("Bucket name must be between 3 and 63 characters")
    if not all(c.isalnum() or c in "-." for c in bucket_name):
        raise ValueError("Bucket name must contain only alphanumeric characters, hyphens, and dots")
    return bucket_name


def build_s3_uri(bucket, key):
    """Build a standard S3 URI string."""
    return f"s3://{bucket}/{key}"


def parse_s3_uri(uri):
    """Parse an S3 URI into bucket and key components."""
    if not uri.startswith("s3://"):
        raise ValueError("Invalid S3 URI: must start with s3://")
    parts = uri[5:].split("/", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("Invalid S3 URI format: expected s3://bucket/key")
    return parts[0], parts[1]
