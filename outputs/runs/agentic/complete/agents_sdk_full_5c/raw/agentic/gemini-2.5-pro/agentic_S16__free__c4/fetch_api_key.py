import os
import boto3
from botocore.exceptions import ClientError

from security_client import get_aws_client

def fetch_api_key(secret_name: str) -> str | None:
    """
    Fetches a secret (like an API key) from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to retrieve.

    Returns:
        The secret string value, or None if an error occurs.
    """
    secretsmanager_client = get_aws_client('secretsmanager')
    
    try:
        response = secretsmanager_client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None
    
    # Depending on whether the secret is a string or binary, one of these fields will be populated
    if 'SecretString' in response:
        return response['SecretString']
    
    # In this context, we assume API keys are strings, not binary.
    print(f"Secret {secret_name} is binary, not a string. Cannot fetch as API key.")
    return None

