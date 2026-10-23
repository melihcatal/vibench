import os
import boto3
from botocore.exceptions import ClientError

def get_s3_client():
    """Initializes and returns a boto3 S3 client."""
    # Using environment variables for credentials is a standard practice for boto3
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
    # AWS_REGION or region_name can be set here or in ~/.aws/config
    return boto3.client(
        's3',
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

def get_storage_bucket():
    """Gets the default storage bucket name from environment variables."""
    bucket_name = os.environ.get("STORAGE_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("STORAGE_BUCKET_NAME environment variable not set.")
    return bucket_name
