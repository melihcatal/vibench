import os
import boto3
from botocore.config import Config

def get_storage_client():
    """
    Initializes and returns a Boto3 S3 client.
    Credentials and region are sourced from environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION
    """
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        config=Config(signature_version='s3v4')
    )

def get_bucket_name():
    """
    Returns the S3 bucket name from the environment variable S3_BUCKET_NAME.
    """
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable not set.")
    return bucket_name
