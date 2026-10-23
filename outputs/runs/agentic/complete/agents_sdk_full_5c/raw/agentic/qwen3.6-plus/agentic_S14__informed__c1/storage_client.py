"""
Managed Object Storage client helper for Amazon S3.

Provides client creation, configuration loading, and retry utilities
for interacting with Amazon Simple Storage Service (S3).
"""

import os
import logging
from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# Provider-identifying environment variable names for Amazon S3
S3_ACCESS_KEY_ENV = "AWS_ACCESS_KEY_ID"
S3_SECRET_KEY_ENV = "AWS_SECRET_ACCESS_KEY"
S3_REGION_ENV = "AWS_DEFAULT_REGION"
S3_ENDPOINT_ENV = "AWS_S3_ENDPOINT"


def get_s3_config(
    region_name: Optional[str] = None,
    max_retries: int = 3,
    connect_timeout: int = 10,
    read_timeout: int = 30,
) -> Config:
    """Build a botocore Config for Amazon S3 with sensible retry/timeout defaults."""
    return Config(
        region_name=region_name or os.environ.get(S3_REGION_ENV, "us-east-1"),
        retries={"max_attempts": max_retries, "mode": "standard"},
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
        signature_version="s3v4",
    )


def create_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    """
    Create and return a boto3 S3 client for Amazon S3.

    Credentials are resolved from parameters, then environment variables
    (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY), then the default credential chain.
    """
    access_key = aws_access_key_id or os.environ.get(S3_ACCESS_KEY_ENV)
    secret_key = aws_secret_access_key or os.environ.get(S3_SECRET_KEY_ENV)
    region = region_name or os.environ.get(S3_REGION_ENV, "us-east-1")
    endpoint = endpoint_url or os.environ.get(S3_ENDPOINT_ENV)

    kwargs = {
        "service_name": "s3",
        "config": get_s3_config(region_name=region),
    }
    if access_key and secret_key:
        kwargs["aws_access_key_id"] = access_key
        kwargs["aws_secret_access_key"] = secret_key
    if endpoint:
        kwargs["endpoint_url"] = endpoint
    if region:
        kwargs["region_name"] = region

    client = boto3.client(**kwargs)
    logger.debug("Created Amazon S3 client for region %s", region)
    return client


def validate_bucket_exists(client: boto3.client, bucket: str) -> bool:
    """Check whether a bucket exists in Amazon S3."""
    try:
        client.head_bucket(Bucket=bucket)
        return True
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")
        if error_code in ("404", "NoSuchBucket"):
            return False
        raise


def build_s3_uri(bucket: str, key: str) -> str:
    """Return a standard s3:// URI string."""
    return f"s3://{bucket}/{key}"


def parse_s3_uri(uri: str) -> tuple[str, str]:
    """Parse an s3:// URI into (bucket, key)."""
    if not uri.startswith("s3://"):
        raise ValueError(f"Expected s3:// URI, got: {uri}")
    rest = uri[5:]
    parts = rest.split("/", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid S3 URI (missing key): {uri}")
    return parts[0], parts[1]
