"""Read a specific secret version or staged value from AWS Secrets Manager."""

import os
import boto3
from botocore.exceptions import ClientError

from security_client import get_secret_manager_client, resolve_secret_name
from security_models import SecretFetchResponse


def rotate_secret_version(
    secret_name: str | None = None,
    version_id: str | None = None,
    version_stage: str = "AWSCURRENT",
) -> SecretFetchResponse:
    """Retrieve a specific version of a secret from AWS Secrets Manager.

    Provider: AWS Secrets Manager (boto3)
    Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

    If version_id is provided, fetches that exact version.
    If version_stage is provided (e.g. AWSCURRENT, AWSPENDING),
    fetches the version matching that stage.
    """
    target_name = resolve_secret_name(secret_name, default_env="ROTATABLE_SECRET_NAME")
    client = get_secret_manager_client()

    kwargs: dict = {"SecretId": target_name}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage and not version_id:
        kwargs["VersionStage"] = version_stage

    try:
        response = client.get_secret_value(**kwargs)
        secret_value = response["SecretString"]

        version_stages = response.get("VersionStages", [])
        return SecretFetchResponse(
            secret_name=target_name,
            secret_value=secret_value,
            version_id=response.get("VersionId"),
            metadata={
                "version_stages": version_stages,
                "requested_stage": version_stage,
                "is_current": "AWSCURRENT" in version_stages,
            },
            provider="aws_secrets_manager",
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        return SecretFetchResponse(
            secret_name=target_name,
            secret_value=None,
            error=f"AWS Secrets Manager error: {error_code} - {exc.response['Error']['Message']}",
            provider="aws_secrets_manager",
        )


def trigger_rotation(secret_name: str | None = None) -> SecretFetchResponse:
    """Trigger AWS Secrets Manager to rotate the secret.

    Provider: AWS Secrets Manager (boto3)
    """
    target_name = resolve_secret_name(secret_name, default_env="ROTATABLE_SECRET_NAME")
    client = get_secret_manager_client()

    try:
        client.rotate_secret(SecretId=target_name)
        return SecretFetchResponse(
            secret_name=target_name,
            secret_value=None,
            metadata={"rotation_triggered": True},
            provider="aws_secrets_manager",
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        return SecretFetchResponse(
            secret_name=target_name,
            secret_value=None,
            error=f"AWS Secrets Manager rotation error: {error_code}",
            provider="aws_secrets_manager",
        )


if __name__ == "__main__":
    result = rotate_secret_version(version_stage="AWSPENDING")
    if result.error:
        print(f"Error: {result.error}")
    else:
        print(f"Version {result.version_id} retrieved for {result.secret_name}")
