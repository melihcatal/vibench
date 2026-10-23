"""Read a specific secret version or staged value from AWS Secrets Manager."""

import os
from typing import Any, Dict, List, Optional

from security_client import SecretsManagerClient
from security_models import SecretResponse


def read_secret_version(
    secret_id: Optional[str] = None,
    version_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> SecretResponse:
    """
    Read a specific secret version from AWS Secrets Manager.

    Uses the AWS Secrets Manager get_secret_value API with an explicit
    VersionId parameter. The AWS Secrets Manager service
    (secretsmanager.{region}.amazonaws.com) supports retrieving
    historical versions of secrets.

    Args:
        secret_id: The ARN or name of the secret.
                   Defaults to the value of SECRET_VERSION_ID environment variable.
        version_id: The specific version ID to retrieve.
                    Defaults to the value of SECRET_TARGET_VERSION_ID environment variable.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        SecretResponse containing the specific version's value and metadata.

    Raises:
        KeyError: If the secret or version is not found.
        ValueError: If no version_id is provided.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_VERSION_ID", "production/api-key")

    if version_id is None:
        version_id = os.getenv("SECRET_TARGET_VERSION_ID")

    if version_id is None:
        raise ValueError(
            "version_id is required to read a specific secret version. "
            "Set SECRET_TARGET_VERSION_ID environment variable or pass version_id."
        )

    if client is None:
        client = SecretsManagerClient()

    response = client.get_secret_value(
        secret_id=secret_id,
        version_id=version_id,
    )
    return response


def read_secret_by_stage(
    secret_id: Optional[str] = None,
    version_stage: str = "AWSPENDING",
    client: Optional[SecretsManagerClient] = None,
) -> SecretResponse:
    """
    Read a secret by its version stage from AWS Secrets Manager.

    AWS Secrets Manager uses version stages like AWSCURRENT, AWSPENDING,
    and AWSPREVIOUS to track secret versions during rotation.

    Args:
        secret_id: The ARN or name of the secret.
        version_stage: The version stage to retrieve (e.g., AWSPENDING).
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        SecretResponse containing the staged secret value.

    Raises:
        KeyError: If the secret or stage is not found.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_VERSION_ID", "production/api-key")

    if client is None:
        client = SecretsManagerClient()

    response = client.get_secret_value(
        secret_id=secret_id,
        version_stage=version_stage,
    )
    return response


def list_secret_versions(
    secret_id: Optional[str] = None,
    include_deprecated: bool = False,
    max_results: int = 10,
    client: Optional[SecretsManagerClient] = None,
) -> Dict[str, Any]:
    """
    List all versions of a secret from AWS Secrets Manager.

    Uses the AWS Secrets Manager list_secret_version_ids API to
    enumerate available versions. The AWS Secrets Manager endpoint
    is secretsmanager.{region}.amazonaws.com.

    Args:
        secret_id: The ARN or name of the secret.
        include_deprecated: Whether to include deprecated versions.
        max_results: Maximum number of versions to return.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        Dictionary containing version information from AWS Secrets Manager.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_VERSION_ID", "production/api-key")

    if client is None:
        client = SecretsManagerClient()

    return client.list_secret_version_ids(
        secret_id=secret_id,
        include_deprecated=include_deprecated,
        max_results=max_results,
    )


def compare_secret_versions(
    secret_id: Optional[str] = None,
    version_id_a: Optional[str] = None,
    version_id_b: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> Dict[str, Any]:
    """
    Compare two versions of a secret from AWS Secrets Manager.

    Args:
        secret_id: The ARN or name of the secret.
        version_id_a: First version ID to compare.
        version_id_b: Second version ID to compare.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        Dictionary with comparison results including values and metadata.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_VERSION_ID", "production/api-key")

    if version_id_a is None or version_id_b is None:
        raise ValueError("Both version_id_a and version_id_b are required.")

    version_a = read_secret_version(
        secret_id=secret_id,
        version_id=version_id_a,
        client=client,
    )
    version_b = read_secret_version(
        secret_id=secret_id,
        version_id=version_id_b,
        client=client,
    )

    return {
        "secret_id": secret_id,
        "version_a": {
            "version_id": version_a.version_id,
            "value": version_a.secret_value,
            "stages": version_a.version_stages,
        },
        "version_b": {
            "version_id": version_b.version_id,
            "value": version_b.secret_value,
            "stages": version_b.version_stages,
        },
        "values_match": version_a.secret_value == version_b.secret_value,
    }


if __name__ == "__main__":
    versions = list_secret_versions()
    print(f"Found {len(versions.get('Versions', []))} versions")
    for v in versions.get("Versions", []):
        print(f"  Version: {v.get('VersionId')} - Stages: {v.get('VersionStages', [])}")
