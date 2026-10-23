import os
import boto3
from security_client import SecretClient

def fetch_api_key(secret_id: str) -> str:
    """Fetches an API key from AWS Secrets Manager.

    Args:
        secret_id: The ARN or friendly name of the secret.

    Returns:
        The stored API key as a string.
    """
    client = SecretClient()  # Uses AWS SDK (boto3) configured via environment variables
    response = client.get_secret_value(SecretId=secret_id)
    return response['SecretString']
