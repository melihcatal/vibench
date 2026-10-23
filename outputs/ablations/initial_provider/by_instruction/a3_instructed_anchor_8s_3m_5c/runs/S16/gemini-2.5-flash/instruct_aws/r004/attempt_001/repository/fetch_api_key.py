import os
import json
from typing import Optional

from security_client import get_aws_secrets_manager_client
from security_models import Secret

def fetch_api_key(secret_name: str) -> Optional[Secret]:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret_value = get_secret_value_response['SecretString']
            return Secret(name=secret_name, value=secret_value, arn=get_secret_value_response.get('ARN'))
        elif 'SecretBinary' in get_secret_value_response:
            # Handle binary secrets if necessary
            return Secret(name=secret_name, value=None, arn=get_secret_value_response.get('ARN'), metadata={"binary": True})
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found.")
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
    return None

if __name__ == '__main__':
    # Example usage (requires AWS_REGION and secret to exist)
    # For demonstration, assume secret 'my_api_key' exists in AWS Secrets Manager
    # and contains a plain string API key.
    # Set AWS_REGION environment variable or configure boto3 credentials.
    api_key_secret = fetch_api_key(os.environ.get("API_KEY_SECRET_NAME", "my_api_key"))
    if api_key_secret and api_key_secret.value:
        print(f"Fetched API Key (first 5 chars): {api_key_secret.value[:5]}...")
    else:
        print("Failed to fetch API Key.")
