"""Read a specific secret version or staged value from AWS Secrets Manager."""

import os
import json
import boto3
from botocore.exceptions import ClientError
from security_client import get_secrets_client
from security_models import SecretFetchResult, SecretError


def read_secret_version(
    secret_id: str,
    version_id: str = None,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> SecretFetchResult:
    """Read a specific version or staged value from AWS Secrets Manager.

    Args:
        secret_id: The name or ARN of the secret.
        version_id: Specific version UUID. If None, uses version_stage.
        version_stage: Staging label such as AWSCURRENT, AWSPENDING, or AWSPREVIOUS.
        region: AWS region override.

    Returns:
        SecretFetchResult with the retrieved secret value and metadata.
    """
    try:
        client = get_secrets_client(region=region)
        params = {"SecretId": secret_id}
        if version_id:
            params["VersionId"] = version_id
        else:
            params["VersionStage"] = version_stage

        response = client.get_secret_value(**params)
        secret_value = response.get("SecretString", "")
        return SecretFetchResult(
            secret_id=secret_id,
            secret_value=secret_value,
            version_id=response.get("VersionId", ""),
            version_stages=response.get("VersionStages", []),
            provider="aws_secrets_manager",
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        raise SecretError(
            secret_id=secret_id,
            message=f"AWS Secrets Manager error reading version: {error_code}",
            error_code=error_code,
        )


def read_pending_version(secret_id: str, region: str = None) -> SecretFetchResult:
    """Read the AWSPENDING staged version from AWS Secrets Manager.

    Used during rotation to inspect the pending secret before it becomes current.
    """
    return read_secret_version(
        secret_id=secret_id,
        version_stage="AWSPENDING",
        region=region,
    )


def read_previous_version(secret_id: str, region: str = None) -> SecretFetchResult:
    """Read the AWSPREVIOUS staged version from AWS Secrets Manager."""
    return read_secret_version(
        secret_id=secret_id,
        version_stage="AWSPREVIOUS",
        region=region,
    )


def get_secret_version_history(
    secret_id: str, region: str = None
) -> list[dict]:
    """Get version history metadata for a secret from AWS Secrets Manager.

    Returns list of version metadata dicts with VersionId, VersionStages, and CreatedDate.
    """
    try:
        client = get_secrets_client(region=region)
        response = client.describe_secret(SecretId=secret_id)
        versions = response.get("VersionIdsToStages", {})
        history = []
        for version_id, stages in versions.items():
            history.append(
                {
                    "version_id": version_id,
                    "stages": stages,
                    "provider": "aws_secrets_manager",
                }
            )
        return history
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        raise SecretError(
            secret_id=secret_id,
            message=f"AWS Secrets Manager error describing secret: {error_code}",
            error_code=error_code,
        )


if __name__ == "__main__":
    secret_id = os.environ.get("SECRET_ID", "prod/api/rotating-key")
    current = read_secret_version(secret_id, version_stage="AWSCURRENT")
    print(f"Current version: {current.version_id}")
    history = get_secret_version_history(secret_id)
    print(f"Version history: {len(history)} versions in AWS Secrets Manager")
