"""
fetch_api_key.py - Fetches an API key from AWS Secrets Manager.

Provider: AWS Secrets Manager
SDK: boto3
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Service hostname: secretsmanager.<region>.amazonaws.com
"""

import os
import logging
from typing import Optional

from security_client import get_secrets_manager_client, retry_with_backoff, validate_secret_name
from security_models import SecretResponse, normalize_secret_response

logger = logging.getLogger(__name__)


def fetch_api_key(secret_name: Optional[str] = None) -> SecretResponse:
    """
    Retrieve an API key stored in AWS Secrets Manager.

    Args:
        secret_name: The name of the secret in AWS Secrets Manager.
                     Defaults to the value of the API_KEY_SECRET_NAME env var.

    Returns:
        SecretResponse containing the fetched API key string.

    Raises:
        ValueError: If no secret name is provided.
        ClientError: On AWS API errors.
    """
    secret_name = secret_name or os.environ.get("API_KEY_SECRET_NAME", "")
    if not validate_secret_name(secret_name):
        raise ValueError(f"Invalid or missing secret name: {secret_name!r}")

    client = get_secrets_manager_client()

    def _get_secret():
        return client.get_secret_value(SecretId=secret_name)

    raw_response = retry_with_backoff(_get_secret)

    secret_resp = normalize_secret_response(raw_response, secret_name)
    logger.info("Fetched API key secret '%s' (version %s)", secret_name, secret_resp.version_id)
    return secret_resp


def get_api_key_value(secret_name: Optional[str] = None) -> str:
    """
    Convenience wrapper that returns just the secret string value.

    Returns the API key as a plain string.
    """
    resp = fetch_api_key(secret_name)
    if resp.secret_string is None:
        raise RuntimeError("Secret string is empty or missing")
    return resp.secret_string
