import os
import boto3
from botocore.exceptions import ClientError
from security_client import get_aws_client

def fetch_api_key(secret_name: str) -> str | None:
    """
    Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to fetch.

    Returns:
        The secret string or None if an error occurs.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    secrets_manager_client = get_aws_client('secretsmanager', region_name)

    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle exceptions such as ResourceNotFoundException
        print(f"Error fetching secret {secret_name}: {e}")
        return None
    
    # Decrypts secret using the associated KMS key.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return secret
    else:
        # If the secret is binary, you might need to decode it
        # decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        print("Secret is binary, not a string.")
        return None
