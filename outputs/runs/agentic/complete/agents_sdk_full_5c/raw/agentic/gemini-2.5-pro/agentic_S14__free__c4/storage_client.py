import os
import boto3
from botocore.client import Config

_S3_CLIENT = None

def get_storage_client():
    """
    Initializes and returns a singleton S3 client.
    Configuration is loaded from environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION
    - S3_ENDPOINT_URL (optional, for custom endpoints)
    """
    global _S3_CLIENT
    if _S3_CLIENT is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
        endpoint_url = os.environ.get("S3_ENDPOINT_URL")

        _S3_CLIENT = boto3.client(
            "s3",
            region_name=region_name,
            endpoint_url=endpoint_url,
            config=Config(signature_version="s3v4"),
        )
    return _S3_CLIENT

def get_bucket_name():
    """
    Returns the configured S3 bucket name from the environment.
    """
    bucket = os.environ.get("S3_BUCKET_NAME")
    if not bucket:
        raise ValueError("S3_BUCKET_NAME environment variable not set.")
    return bucket
