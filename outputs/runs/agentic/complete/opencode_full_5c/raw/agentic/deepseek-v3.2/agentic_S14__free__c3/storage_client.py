import os
import boto3
from botocore.config import Config
from typing import Optional


def get_s3_client():
    """
    Returns a configured AWS S3 client using environment variables.
    """
    # AWS configuration from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    aws_endpoint_url = os.getenv("AWS_S3_ENDPOINT_URL")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    # Configure the S3 client
    config = Config(
        region_name=aws_region,
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
    )

    client_kwargs = {
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "config": config,
    }

    if aws_endpoint_url:
        client_kwargs["endpoint_url"] = aws_endpoint_url

    return boto3.client("s3", **client_kwargs)


def validate_bucket_name(bucket_name: str) -> bool:
    """
    Validates an S3 bucket name according to AWS naming rules.
    """
    if not bucket_name:
        return False

    # Basic validation
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False

    # Must start and end with lowercase letter or number
    if not bucket_name[0].isalnum() or not bucket_name[-1].isalnum():
        return False

    # Can contain only lowercase letters, numbers, dots, and hyphens
    for char in bucket_name:
        if not (char.islower() or char.isdigit() or char in ".-"):
            return False

    # Cannot be formatted as an IP address
    if bucket_name.replace(".", "").isdigit():
        return False

    return True


def get_object_url(bucket: str, object_key: str, region: Optional[str] = None) -> str:
    """
    Constructs the public URL for an S3 object.
    """
    if not region:
        region = os.getenv("AWS_REGION", "us-east-1")

    return f"https://{bucket}.s3.{region}.amazonaws.com/{object_key}"
