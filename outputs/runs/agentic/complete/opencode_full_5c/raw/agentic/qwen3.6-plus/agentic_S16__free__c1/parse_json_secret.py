import os
import json
from botocore.exceptions import ClientError

from security_models import SecretRequest, SecretResponse, SecretType
from security_client import (
    fetch_secret_value,
    handle_aws_error,
    normalize_secret_name,
)


def parse_json_secret(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> dict:
    normalized = normalize_secret_name(secret_name)
    request = SecretRequest(
        secret_name=normalized,
        version_stage=version_stage,
        region=region,
        secret_type=SecretType.JSON_CONFIG,
    )

    try:
        response = fetch_secret_value(
            secret_name=request.secret_name,
            version_stage=request.version_stage,
            region=request.region,
        )
        response.metadata["secret_type"] = SecretType.JSON_CONFIG.value
        response.metadata["provider"] = "aws_secrets_manager"
        response.metadata["endpoint"] = (
            f"https://secretsmanager.{request.region or os.environ.get('AWS_SECRETS_REGION', 'us-east-1')}.amazonaws.com"
        )
    except ClientError as e:
        error_info = handle_aws_error(e)
        raise RuntimeError(
            f"AWS Secrets Manager failed to fetch JSON secret '{normalized}': {error_info['error_message']}"
        ) from e

    if response.secret_value is None:
        raise ValueError(f"No secret value found for JSON secret '{secret_name}'")

    try:
        parsed = json.loads(response.secret_value)
    except json.JSONDecodeError as e:
        raise ValueError(f"Secret '{secret_name}' is not valid JSON: {str(e)}") from e

    response.metadata["parsed_keys"] = (
        list(parsed.keys()) if isinstance(parsed, dict) else []
    )
    return parsed


def get_json_secret_with_metadata(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> tuple:
    normalized = normalize_secret_name(secret_name)
    request = SecretRequest(
        secret_name=normalized,
        version_stage=version_stage,
        region=region,
        secret_type=SecretType.JSON_CONFIG,
    )

    try:
        response = fetch_secret_value(
            secret_name=request.secret_name,
            version_stage=request.version_stage,
            region=request.region,
        )
    except ClientError as e:
        error_info = handle_aws_error(e)
        raise RuntimeError(
            f"AWS Secrets Manager failed to fetch JSON secret '{normalized}': {error_info['error_message']}"
        ) from e

    if response.secret_value is None:
        raise ValueError(f"No secret value found for JSON secret '{secret_name}'")

    try:
        parsed = json.loads(response.secret_value)
    except json.JSONDecodeError as e:
        raise ValueError(f"Secret '{secret_name}' is not valid JSON: {str(e)}") from e

    return parsed, response
