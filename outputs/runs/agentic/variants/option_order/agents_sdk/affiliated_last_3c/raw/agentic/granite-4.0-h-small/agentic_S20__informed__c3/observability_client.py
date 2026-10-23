import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def get_cloudwatch_logs_client() -> boto3.client:
    """Create and cache a CloudWatch Logs client using AWS credentials from environment variables."""
    region = os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client(
        "logs",
        region_name=region,
        # boto3 will read AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from env by default
    )
    return client

# Simple singleton pattern for demo purposes
_log_client = None

def get_cached_client() -> boto3.client:
    global _log_client
    if _log_client is None:
        _log_client = get_cloudwatch_logs_client()
    return _log_client
