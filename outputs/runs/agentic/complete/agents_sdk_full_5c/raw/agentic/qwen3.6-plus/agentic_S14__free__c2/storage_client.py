"""
Managed Object Storage client configuration and helper utilities.

Uses AWS S3 (boto3) as the concrete managed object storage provider.
"""

import os
import boto3
from botocore.config import Config
from typing import Optional

S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", None)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME", "")
DEFAULT_PRESIGNED_URL_EXPIRY = int(os.environ.get("PRESIGNED_URL_EXPIRY_SECONDS", "3600"))


def get_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    """Create and return a configured boto3 S3 client."""
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id or AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_secret_access_key or AWS_SECRET_ACCESS_KEY,
        region_name=region_name or AWS_DEFAULT_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        signature_version="s3v4",
    )
    client = session.client(
        "s3",
        config=config,
        endpoint_url=endpoint_url or S3_ENDPOINT_URL,
    )
    return client


def get_bucket_name(bucket: Optional[str] = None) -> str:
    """Resolve the target bucket name from parameter or environment."""
    resolved = bucket or AWS_BUCKET_NAME
    if not resolved:
        raise ValueError("Bucket name must be provided or set via AWS_BUCKET_NAME")
    return resolved


def validate_object_key(key: str) -> None:
    """Validate an S3 object key."""
    if not key or key.startswith("/") or key.endswith("/"):
        raise ValueError(f"Invalid object key: '{key}'. Keys must not be empty, start with '/', or end with '/'")
    if len(key) > 1024:
        raise ValueError(f"Object key exceeds 1024 character limit: '{key[:100]}...'")
