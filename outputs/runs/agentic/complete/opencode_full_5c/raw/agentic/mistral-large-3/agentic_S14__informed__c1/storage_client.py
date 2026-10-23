import os
from typing import Optional

import boto3
from botocore.client import Config


def get_storage_client():
    """
    Initializes and returns an Amazon S3 client with optional configuration.

    Environment Variables:
        AWS_ACCESS_KEY_ID: AWS access key ID.
        AWS_SECRET_ACCESS_KEY: AWS secret access key.
        AWS_REGION: AWS region name.
        AWS_ENDPOINT_URL: Optional custom endpoint URL.

    Returns:
        Configured boto3 S3 client.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")
    endpoint_url = os.getenv("AWS_ENDPOINT_URL")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found in environment variables. "
            "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        )

    config = Config(
        signature_version="s3v4",
        retries={
            "max_attempts": 3,
            "mode": "standard",
        },
    )

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        endpoint_url=endpoint_url,
        config=config,
    )
