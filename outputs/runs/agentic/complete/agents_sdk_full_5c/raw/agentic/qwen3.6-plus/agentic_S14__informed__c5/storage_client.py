"""
storage_client.py - Local configuration and client helper utilities for Managed Object Storage.

Uses Amazon S3 (boto3) as the concrete managed object storage provider.
Authentication via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
"""

import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Optional


def get_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    """
    Create and return an Amazon S3 client using boto3.

    Args:
        aws_access_key_id: AWS access key ID. Falls back to AWS_ACCESS_KEY_ID env var.
        aws_secret_access_key: AWS secret access key. Falls back to AWS_SECRET_ACCESS_KEY env var.
        region_name: AWS region name. Defaults to 'us-east-1'.
        endpoint_url: Optional custom endpoint URL (for S3-compatible services).

    Returns:
        Configured boto3 S3 client.
    """
    access_key = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    config = Config(
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
    )

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    client_kwargs = {"config": config}
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url

    s3_client = session.client("s3", **client_kwargs)
    return s3_client


def validate_bucket_exists(s3_client: boto3.client, bucket_name: str) -> bool:
    """
    Check if an S3 bucket exists and is accessible.

    Args:
        s3_client: boto3 S3 client.
        bucket_name: Name of the S3 bucket to validate.

    Returns:
        True if bucket exists, False otherwise.
    """
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False


def create_bucket_if_not_exists(
    s3_client: boto3.client, bucket_name: str, region: str = "us-east-1"
) -> bool:
    """
    Create an S3 bucket if it does not already exist.

    Args:
        s3_client: boto3 S3 client.
        bucket_name: Name of the S3 bucket to create.
        region: AWS region for bucket creation.

    Returns:
        True if bucket was created or already exists, False on error.
    """
    if validate_bucket_exists(s3_client, bucket_name):
        return True

    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        return True
    except ClientError as e:
        print(f"Error creating bucket {bucket_name}: {e}")
        return False
