import os
from typing import Optional

import boto3
from botocore.client import Config


def get_storage_client():
    """
    Initialize and return an S3 client using boto3 with AWS credentials.
    """
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    client = session.client(
        "s3",
        config=Config(signature_version="s3v4"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    return client


def get_bucket_name() -> str:
    """
    Retrieve the bucket name from environment variables.
    """
    return os.getenv("AWS_S3_BUCKET_NAME")