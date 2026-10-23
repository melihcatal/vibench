# storage_client.py
# Helper utilities for Managed Object Storage

import os
from typing import Any, Dict

# Example using Amazon S3 with boto3 SDK
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_s3_client() -> boto3.client:"""Create and return an S3 client with environment credentials.

Credentials expected:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_DEFAULT_REGION (optional)
"""
    try:
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=region,
        )
        return client
    except (NoCredentialsError, PartialCredentialsError) as exc:
        raise RuntimeError(
            "S3 client configuration error: missing AWS credentials"
        ) from exc

# Add more SDK client creators here if needed (e.g., Backblaze B2, Alibaba OSS)
