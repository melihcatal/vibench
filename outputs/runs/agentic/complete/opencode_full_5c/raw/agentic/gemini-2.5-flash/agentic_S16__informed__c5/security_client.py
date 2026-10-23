import os
import boto3
from typing import Any


def get_secrets_manager_client() -> Any:
    """Initializes and returns an AWS Secrets Manager client."""
    # AWS_REGION_NAME can be optionally set in environment variables
    region_name = os.getenv("AWS_REGION_NAME", "us-east-1")
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are typically picked up
    # from environment variables or IAM roles automatically by boto3.
    # Explicit credentials can also be passed if needed, but relying on env/roles is common.
    client = boto3.client("secretsmanager", region_name=region_name)
    return client
