"""
fetch_api_key.py - Fetches an API key from AWS Secrets Manager.

Uses boto3 to connect to secretsmanager.amazonaws.com and retrieve
an API key secret by name, with version stage support.
"""

from __future__ import annotations

import logging
from typing import Optional

from security_client import get_secretsmanager_client, get_secret_value
from security_models import SecretResponse, describe_secret

logger = logging.getLogger(__name__)


def fetch_api_key(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
) -> SecretResponse:
    """
    Fetch an API key stored in AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret containing the API key.
        version_stage: The version stage to retrieve (default AWSCURRENT).
        region: AWS region override.

    Returns:
        SecretResponse with the API key value and metadata.
    """
    client = get_secretsmanager_client(region_name=region)
    logger.info("Fetching API key from AWS Secrets Manager: %s (stage=%s)", secret_name, version_stage)

    secret_value_resp = get_secret_value(
        client,
        secret_id=secret_name,
        version_stage=version_stage,
    )

    metadata = describe_secret(client, secret_name)

    return SecretResponse.from_aws_response(secret_value_resp, metadata)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    secret_name_env = "production/api/stripe-key"
    result = fetch_api_key(secret_name_env)
    logger.info("Fetched secret: %s (version=%s)", result.name, result.version_id)
    print(f"API key secret name: {result.name}")
    print(f"Version ID: {result.version_id}")
    print(f"Value length: {len(result.value)}")
