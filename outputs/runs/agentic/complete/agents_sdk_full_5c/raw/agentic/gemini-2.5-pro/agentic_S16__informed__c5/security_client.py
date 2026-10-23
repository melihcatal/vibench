"""Local client helper for Secret Management."""
import os
import boto3
from botocore.client import BaseClient


def get_secrets_manager_client() -> BaseClient:
    """
    Initializes and returns a boto3 client for AWS Secrets Manager.

    Configures the client using environment variables for credentials and region.
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN (optional)
    - AWS_REGION

    Returns:
        A boto3 client for AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    
    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    return client
