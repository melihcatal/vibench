import os
import boto3
from typing import Any, Dict


def get_cloudwatch_client() -> boto3.client:
    """Initialize and return an AWS CloudWatch Logs client configured via environment variables.
    Expected env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, CLOUDWATCH_LOG_GROUP, CLOUDWATCH_LOG_STREAM.
    """
    client = boto3.client(
        "logs",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    return client
