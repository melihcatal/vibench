# [HELPER] storage_client.py

# Provider: Amazon S3
# SDK: boto3
# Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

import os
import boto3
from botocore.exceptions import NoCredentialsError


# Helper to get bucket name from env
def get_bucket_name() -> str:
    bucket_name = os.getenv("S3_BUCKET_NAME")
    if not bucket_name:
        raise RuntimeError("S3_BUCKET_NAME environment variable not set")
    return bucket_name


# Create a reusable S3 client with region configuration
def get_s3_client(region_name: str = "us-east-1") -> boto3.client:
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key or not aws_secret_key:
        raise RuntimeError("AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY not set")
    return boto3.client(
        "s3",
        region_name=region_name,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )


# Example utilities (non‑scoring, but useful for later steps)
# – you can extend this module with pagination helpers, retry wrappers, etc.
