import os
from security_client import get_aws_secrets_manager_client


def fetch_api_key(secret_name: str) -> str:
    """Fetches an API key from AWS Secrets Manager."""
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching secret '{secret_name}': {e}")

    if "SecretString" in get_secret_value_response:
        return get_secret_value_response["SecretString"]
    else:
        # Secrets can also be binary, but for API keys, we expect a string.
        raise TypeError(f"Secret '{secret_name}' did not contain a SecretString.")
