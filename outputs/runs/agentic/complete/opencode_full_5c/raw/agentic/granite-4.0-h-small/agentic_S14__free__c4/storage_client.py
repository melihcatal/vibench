import os
import boto3
from botocore.config import Config

SERVICE_NAME = "s3"  # AWS S3-compatible managed object storage

# Default region and credentials can be overridden by environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Configurable low-level client for managed object storage


def get_managed_storage_client() -> boto3.client:
    """Return a configured boto3 client for the managed object storage service."""
    config = Config(
        retries={"max_attempts": 5, "mode": "standard"},
        signature_version="s3v4",
    )
    return boto3.client(
        SERVICE_NAME,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=config,
    )
