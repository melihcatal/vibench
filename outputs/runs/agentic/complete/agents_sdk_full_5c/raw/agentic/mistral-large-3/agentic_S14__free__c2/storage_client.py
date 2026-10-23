import os
import boto3
from botocore.client import Config

def get_storage_client():
    """
    Provides a configured boto3 S3 client for AWS managed object storage.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        config=Config(signature_version="s3v4")
    )