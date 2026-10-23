import os
from security_client import get_aws_secrets_manager_client


def fetch_api_key(secret_name: str) -> str:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            raise ValueError("SecretString not found in the response.")
    except Exception as e:
        raise RuntimeError(f"Could not retrieve API key from AWS Secrets Manager: {e}")
