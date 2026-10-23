"""
Fetch an API key from AWS Secrets Manager.

This module retrieves a stored API key from a managed secrets store
using the AWS Secrets Manager service.
"""

import json
import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from security_client import get_secrets_manager_client
from security_models import SecretFetchResult

logger = logging.getLogger(__name__)

SECRETS_MANAGER_ENDPOINT = "https://secretsmanager.us-east-1.amazonaws.com"
AWS_PROVIDER_ID = "aws-secrets-manager"


def fetch_api_key(secret_name: str, region_name: str = "us-east-1") -> SecretFetchResult:
    """
    Fetch an API key secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret containing the API key.
        region_name: AWS region for the Secrets Manager endpoint.

    Returns:
        SecretFetchResult with the retrieved API key or error details.
    """
    try:
        client = get_secrets_manager_client(region_name=region_name)

        response = client.get_secret_value(SecretId=secret_name)

        secret_string = response.get("SecretString")
        version_id = response.get("VersionId")
        arn = response.get("ARN")

        if not secret_string:
            return SecretFetchResult(
                success=False,
                secret_name=secret_name,
                provider=AWS_PROVIDER_ID,
                error="Secret value is empty or binary-only",
            )

        result = SecretFetchResult(
            success=True,
            secret_name=secret_name,
            secret_value=secret_string,
            version_id=version_id,
            arn=arn,
            provider=AWS_PROVIDER_ID,
        )

        logger.info("Successfully fetched API key from %s", secret_name)
        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error("AWS Secrets Manager error fetching %s: %s", secret_name, error_code)
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=f"AWS error: {error_code}",
        )
    except Exception as e:
        logger.error("Unexpected error fetching API key %s: %s", secret_name, str(e))
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=str(e),
        )


def fetch_api_key_by_stage(
    secret_name: str, stage: str = "AWSCURRENT", region_name: str = "us-east-1"
) -> SecretFetchResult:
    """
    Fetch an API key from AWS Secrets Manager using a specific staging label.

    Args:
        secret_name: The secret name or ARN.
        stage: The staging label (e.g., AWSCURRENT, AWSPENDING).
        region_name: AWS region.

    Returns:
        SecretFetchResult with the API key or error details.
    """
    try:
        client = get_secrets_manager_client(region_name=region_name)

        response = client.get_secret_value(SecretId=secret_name, VersionStage=stage)

        return SecretFetchResult(
            success=True,
            secret_name=secret_name,
            secret_value=response.get("SecretString"),
            version_id=response.get("VersionId"),
            arn=response.get("ARN"),
            provider=AWS_PROVIDER_ID,
            stage=stage,
        )

    except ClientError as e:
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=f"AWS Secrets Manager error: {e.response['Error']['Code']}",
        )
