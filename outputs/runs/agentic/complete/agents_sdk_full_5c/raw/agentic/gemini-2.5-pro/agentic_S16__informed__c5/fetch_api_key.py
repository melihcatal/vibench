"""Fetches a simple API key from AWS Secrets Manager."""
import os
from typing import Optional

from security_client import get_secrets_manager_client


def fetch_api_key(secret_name: str) -> Optional[str]:
    """
    Fetches a secret string from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.

    Returns:
        The secret string, or None if an error occurs.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return get_secret_value_response.get('SecretString')
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Set the AWS_REGION environment variable, e.g., 'us-east-1'
    # Ensure AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are set.
    api_key_secret_name = os.environ.get("API_KEY_SECRET_NAME")
    if api_key_secret_name:
        api_key = fetch_api_key(api_key_secret_name)
        if api_key:
            print(f"Successfully fetched API key from secret: {api_key_secret_name}")
    else:
        print("Please set the API_KEY_SECRET_NAME environment variable.")
