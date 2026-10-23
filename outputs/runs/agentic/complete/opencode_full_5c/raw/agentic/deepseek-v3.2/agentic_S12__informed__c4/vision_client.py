import os
import boto3
from typing import Optional


def get_vision_client() -> boto3.client:
    """
    Get Amazon Rekognition client with configuration from environment variables.

    Returns:
        boto3 Rekognition client

    Raises:
        ValueError: If AWS credentials are not configured
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not configured. "
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    return session.client("rekognition")
