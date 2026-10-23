import os
from security_client import get_aws_secrets_manager_client


def fetch_api_key(secret_name: str) -> str | None:
    """
    Fetches an API key from AWS Secrets Manager.
    """
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        return None

    secret = get_secret_value_response.get("SecretString")
    return secret
