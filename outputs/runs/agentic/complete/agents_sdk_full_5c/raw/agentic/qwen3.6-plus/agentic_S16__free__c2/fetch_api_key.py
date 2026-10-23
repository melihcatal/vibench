"""Fetch an API key from AWS Secrets Manager managed secrets store."""

import os
from typing import Optional

from security_client import SecretsManagerClient
from security_models import SecretResponse


def fetch_api_key(
    secret_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> SecretResponse:
    """
    Fetch an API key from AWS Secrets Manager.

    Uses the AWS Secrets Manager get_secret_value API to retrieve
    the secret identified by secret_id. The AWS Secrets Manager service
    endpoint is secretsmanager.{region}.amazonaws.com.

    Args:
        secret_id: The ARN or name of the secret containing the API key.
                   Defaults to the value of SECRET_API_KEY_ID environment variable.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        SecretResponse containing the API key value and metadata.

    Raises:
        KeyError: If the secret is not found in AWS Secrets Manager.
        ValueError: If the request to AWS Secrets Manager is invalid.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_API_KEY_ID", "production/api-key")

    if client is None:
        client = SecretsManagerClient()

    response = client.get_secret_value(
        secret_id=secret_id,
        version_stage="AWSCURRENT",
    )
    return response


def fetch_api_key_raw(secret_id: Optional[str] = None) -> str:
    """
    Fetch an API key from AWS Secrets Manager and return just the key string.

    Args:
        secret_id: The ARN or name of the secret containing the API key.

    Returns:
        The raw API key string value.
    """
    response = fetch_api_key(secret_id=secret_id)
    return response.secret_value


if __name__ == "__main__":
    api_key_response = fetch_api_key()
    print(f"Retrieved API key from secret: {api_key_response.secret_id}")
    print(f"Key length: {len(api_key_response.secret_value)}")
    print(f"Version ID: {api_key_response.version_id}")
