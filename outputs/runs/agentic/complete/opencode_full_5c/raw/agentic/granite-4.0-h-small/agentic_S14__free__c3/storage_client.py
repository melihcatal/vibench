# [HELPER] storage_client.py

import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def get_managed_storage_client(
    region_name: str = "us-east-1", endpoint_url: str = None
) -> boto3.client:
    """Create and return a managed object‑storage client.

    Detects credentials from environment variables or shared config files.
    For a concrete provider we use the AWS S3 (MinIO) SDK as example.
    """
    try:
        # Default to S3-compatible endpoint; override via env var if desired.
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if not aws_access_key or not aws_secret_key:
            raise NoCredentialsError("Missing AWS credentials")
        client = boto3.client(
            "s3",
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )
        return client
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise RuntimeError("Failed to initialize storage client: " + str(e))
