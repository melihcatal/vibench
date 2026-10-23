import os
from typing import Optional
from security_client import get_aws_secrets_manager_client
from security_models import Secret

def fetch_api_key_from_aws(secret_name: str) -> Optional[Secret]:
    """
    Fetches a secret string, like an API key, from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.

    Returns:
        A Secret object containing the key, or None if not found.
    """
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        return None

    secret_string = get_secret_value_response.get("SecretString")
    if secret_string:
        return Secret(
            name=secret_name,
            value=secret_string,
            version=get_secret_value_response.get("VersionId"),
        )
    return None
