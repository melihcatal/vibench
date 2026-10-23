"""
fetch_api_key.py - Fetches an API key from a managed secrets store.

Uses AWS Secrets Manager (boto3 SDK) to retrieve a named API key secret
by its secret identifier. Handles AWS-specific error codes and returns
a normalized SecretResponse.

Provider: AWS Secrets Manager (secretsmanager.us-east-1.amazonaws.com)
"""

from __future__ import annotations

import logging
from typing import Optional

from botocore.exceptions import ClientError

from security_client import (
    get_secrets_manager_client,
    resolve_secret_id,
    handle_aws_client_error,
    parse_get_secret_value_response,
)
from security_models import SecretResponse

logger = logging.getLogger(__name__)


def fetch_api_key(
    secret_id: str,
    version_stage: str = "AWSCURRENT",
) -> SecretResponse:
    """
    Fetch an API key secret from AWS Secrets Manager.

    Args:
        secret_id: The secret name or ARN in AWS Secrets Manager.
        version_stage: The staging label (e.g., AWSCURRENT, AWSPENDING).

    Returns:
        SecretResponse containing the retrieved API key value.
    """
    resolved_id = resolve_secret_id(secret_id)
    client = get_secrets_manager_client()

    try:
        response = client.get_secret_value(
            SecretId=resolved_id,
            VersionStage=version_stage,
        )
        return parse_get_secret_value_response(response, resolved_id)
    except ClientError as e:
        return handle_aws_client_error(e, resolved_id)
    except Exception as exc:
        logger.exception("Unexpected error fetching API key secret %s", resolved_id)
        return SecretResponse(
            success=False,
            secret_id=resolved_id,
            error_message=f"Unexpected error: {exc}",
        )


def fetch_api_key_raw(secret_id: str) -> Optional[str]:
    """
    Convenience function to fetch just the API key string value.

    Returns the raw API key string or None on failure.
    """
    result = fetch_api_key(secret_id)
    if result.success:
        return result.secret_value
    logger.warning("Failed to fetch API key %s: %s", secret_id, result.error_message)
    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    secret_name = "prod/api/stripe-key"
    result = fetch_api_key(secret_name)
    if result.success:
        print(f"API key fetched successfully. Version: {result.version_id}")
    else:
        print(f"Failed: {result.error_message}")