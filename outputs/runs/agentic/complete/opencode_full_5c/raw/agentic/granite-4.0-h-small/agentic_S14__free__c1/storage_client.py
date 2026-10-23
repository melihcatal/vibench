# storage_client.py
# [HELPER] Managed Object Storage client utilities and local configuration
import os
import boto3
from typing import Callable

# Environment variables for configuration (fallback defaults provided)
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", None)
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", None)
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", None)
S3_REGION = os.getenv("S3_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET", "default-bucket")


def get_s3_client() -> boto3.client:
    """Create and return a configured S3 client.

    Uses either an endpoint URL (for custom storage services) or the default AWS S3 service.
    """
    if S3_ENDPOINT_URL:
        return boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name=S3_REGION,
        )
    else:
        return boto3.client(
            "s3",
            region_name=S3_REGION,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )


def get_bucket_name() -> str:
    """Retrieve the bucket name from env or return the default fallback."""
    return os.getenv("S3_BUCKET", "default-bucket")
