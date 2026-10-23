"""
rotate_secret_version.py - Reads a specific secret version or staged value from AWS Secrets Manager.

Provider: AWS Secrets Manager
SDK: boto3
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Service hostname: secretsmanager.<region>.amazonaws.com
"""

import os
import logging
from typing import Optional, List

from security_client import get_secrets_manager_client, retry_with_backoff, validate_secret_name
from security_models import SecretResponse, normalize_secret_response

logger = logging.getLogger(__name__)


def get_secret_by_version(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> SecretResponse:
    """
    Retrieve a specific version of a secret from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret.
        version_id: Specific version UUID to fetch.
        version_stage: Stage label (e.g. 'AWSCURRENT', 'AWSPENDING') to resolve.

    Returns:
        SecretResponse for the requested version.

    Raises:
        ValueError: If neither version_id nor version_stage is provided.
        ClientError: On AWS API errors.
    """
    if not validate_secret_name(secret_name):
        raise ValueError(f"Invalid secret name: {secret_name!r}")

    if not version_id and not version_stage:
        raise ValueError("Must provide either version_id or version_stage")

    client = get_secrets_manager_client()
    params: dict = {"SecretId": secret_name}
    if version_id:
        params["VersionId"] = version_id
    if version_stage:
        params["VersionStage"] = version_stage

    def _get_secret():
        return client.get_secret_value(**params)

    raw_response = retry_with_backoff(_get_secret)
    secret_resp = normalize_secret_response(raw_response, secret_name)

    logger.info(
        "Fetched secret '%s' version %s (stages: %s)",
        secret_name,
        secret_resp.version_id,
        secret_resp.version_stages,
    )
    return secret_resp


def get_staged_secret_value(
    secret_name: str,
    stage: str = "AWSCURRENT",
) -> Optional[str]:
    """
    Retrieve the secret string for a given version stage.

    Common stages:
      - AWSCURRENT: The currently active secret version.
      - AWSPENDING: A version being rotated but not yet active.
      - AWSPREVIOUS: The version before the current one.

    Returns the secret string or None if not available.
    """
    resp = get_secret_by_version(secret_name, version_stage=stage)
    return resp.secret_string


def describe_secret_versions(secret_name: str) -> dict:
    """
    Describe a secret and return version-to-stage mapping from AWS Secrets Manager.

    Returns the raw VersionIdsToStages dict from the DescribeSecret API.
    """
    if not validate_secret_name(secret_name):
        raise ValueError(f"Invalid secret name: {secret_name!r}")

    client = get_secrets_manager_client()

    def _describe():
        return client.describe_secret(SecretId=secret_name)

    raw = retry_with_backoff(_describe)
    return raw.get("VersionIdsToStages", {})


def compare_secret_versions(
    secret_name: str,
    version_a: str,
    version_b: str,
) -> bool:
    """
    Compare two specific secret versions and return True if they are identical.
    """
    resp_a = get_secret_by_version(secret_name, version_id=version_a)
    resp_b = get_secret_by_version(secret_name, version_id=version_b)

    if resp_a.secret_string is not None and resp_b.secret_string is not None:
        return resp_a.secret_string == resp_b.secret_string
    if resp_a.secret_binary is not None and resp_b.secret_binary is not None:
        return resp_a.secret_binary == resp_b.secret_binary
    return False
