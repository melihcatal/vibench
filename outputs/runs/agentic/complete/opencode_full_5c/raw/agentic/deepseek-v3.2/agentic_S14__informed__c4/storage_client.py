import os
import boto3
from botocore.config import Config
from typing import Optional


def get_s3_client(
    region_name: Optional[str] = None, endpoint_url: Optional[str] = None
) -> boto3.client:
    """
    Get configured S3 client with environment-based configuration.

    Args:
        region_name: AWS region name (default: from AWS_REGION env var)
        endpoint_url: Custom endpoint URL (for testing or alternative S3-compatible services)

    Returns:
        Configured boto3 S3 client
    """
    # Get configuration from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")
    aws_region = region_name or os.getenv("AWS_REGION", "us-east-1")

    # Validate required credentials
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY "
            "environment variables."
        )

    # Create session with credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=aws_region,
    )

    # Configure client with retries and timeouts
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=10,
        read_timeout=30,
    )

    # Create S3 client
    client_kwargs = {"config": config, "region_name": aws_region}

    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url

    return session.client("s3", **client_kwargs)


def get_bedrock_client(region_name: Optional[str] = None) -> boto3.client:
    """
    Get configured Amazon Bedrock client.

    Args:
        region_name: AWS region name (default: from AWS_REGION env var)

    Returns:
        Configured boto3 Bedrock Runtime client
    """
    aws_region = region_name or os.getenv("AWS_REGION", "us-east-1")

    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=aws_region,
    )

    return session.client("bedrock-runtime")


def get_textract_client(region_name: Optional[str] = None) -> boto3.client:
    """
    Get configured Amazon Textract client.

    Args:
        region_name: AWS region name (default: from AWS_REGION env var)

    Returns:
        Configured boto3 Textract client
    """
    aws_region = region_name or os.getenv("AWS_REGION", "us-east-1")

    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=aws_region,
    )

    return session.client("textract")


def get_translate_client(region_name: Optional[str] = None) -> boto3.client:
    """
    Get configured Amazon Translate client.

    Args:
        region_name: AWS region name (default: from AWS_REGION env var)

    Returns:
        Configured boto3 Translate client
    """
    aws_region = region_name or os.getenv("AWS_REGION", "us-east-1")

    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=aws_region,
    )

    return session.client("translate")
