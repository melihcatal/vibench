import os
from typing import Optional

import boto3
from boto3 import client
from botocore.config import Config


def get_storage_client() -> client:
    """
    Initializes and returns an AWS S3 client with optional configuration.

    Configuration is loaded from environment variables:
    - AWS_ACCESS_KEY_ID: AWS access key.
    - AWS_SECRET_ACCESS_KEY: AWS secret key.
    - AWS_REGION: AWS region (default: "us-east-1").
    - AWS_ENDPOINT_URL: Custom endpoint URL (optional).
    - AWS_S3_SIGNATURE_VERSION: Signature version (default: "s3v4").

    Returns:
        Initialized boto3 S3 client.
    """
    config = Config(
        signature_version=os.getenv("AWS_S3_SIGNATURE_VERSION", "s3v4"),
        retries={
            "max_attempts": 3,
            "mode": "standard",
        },
    )

    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        config=config,
    )
