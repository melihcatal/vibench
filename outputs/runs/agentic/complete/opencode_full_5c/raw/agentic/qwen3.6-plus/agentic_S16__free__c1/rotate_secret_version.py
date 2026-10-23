import os
from botocore.exceptions import ClientError

from security_models import SecretRequest, SecretResponse
from security_client import (
    fetch_secret_value,
    describe_secret,
    list_secret_version_ids,
    handle_aws_error,
    normalize_secret_name,
)


def rotate_secret_version(
    secret_name: str,
    version_id: str = None,
    version_stage: str = "AWSPENDING",
    region: str = None,
) -> SecretResponse:
    normalized = normalize_secret_name(secret_name)
    request = SecretRequest(
        secret_name=normalized,
        version_id=version_id,
        version_stage=version_stage,
        region=region,
    )

    try:
        response = fetch_secret_value(
            secret_name=request.secret_name,
            version_id=request.version_id,
            version_stage=request.version_stage,
            region=request.region,
        )
        response.metadata["provider"] = "aws_secrets_manager"
        response.metadata["endpoint"] = (
            f"https://secretsmanager.{request.region or os.environ.get('AWS_SECRETS_REGION', 'us-east-1')}.amazonaws.com"
        )
        return response
    except ClientError as e:
        error_info = handle_aws_error(e)
        raise RuntimeError(
            f"AWS Secrets Manager failed to read version for '{normalized}': {error_info['error_message']}"
        ) from e


def get_staged_secret_value(
    secret_name: str,
    stage: str = "AWSPENDING",
    region: str = None,
) -> SecretResponse:
    return rotate_secret_version(secret_name, version_stage=stage, region=region)


def list_available_versions(
    secret_name: str,
    region: str = None,
) -> list:
    normalized = normalize_secret_name(secret_name)
    try:
        versions = list_secret_version_ids(normalized, region)
        result = []
        for v in versions:
            result.append(
                {
                    "version_id": v.get("VersionId"),
                    "version_stages": v.get("VersionStages", []),
                    "created_date": v.get("CreatedDate", "").isoformat()
                    if v.get("CreatedDate")
                    else None,
                }
            )
        return result
    except ClientError as e:
        error_info = handle_aws_error(e)
        raise RuntimeError(
            f"AWS Secrets Manager failed to list versions for '{normalized}': {error_info['error_message']}"
        ) from e


def get_secret_version_by_id(
    secret_name: str,
    version_id: str,
    region: str = None,
) -> SecretResponse:
    return rotate_secret_version(secret_name, version_id=version_id, region=region)
