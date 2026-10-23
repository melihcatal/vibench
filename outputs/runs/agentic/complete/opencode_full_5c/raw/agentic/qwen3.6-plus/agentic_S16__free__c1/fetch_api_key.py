import os
from botocore.exceptions import ClientError

from security_models import SecretRequest, SecretResponse, SecretType
from security_client import (
    fetch_secret_value,
    handle_aws_error,
    normalize_secret_name,
)


def fetch_api_key(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> SecretResponse:
    normalized = normalize_secret_name(secret_name)
    request = SecretRequest(
        secret_name=normalized,
        version_stage=version_stage,
        region=region,
        secret_type=SecretType.API_KEY,
    )

    try:
        response = fetch_secret_value(
            secret_name=request.secret_name,
            version_stage=request.version_stage,
            region=request.region,
        )
        response.metadata["secret_type"] = SecretType.API_KEY.value
        response.metadata["provider"] = "aws_secrets_manager"
        response.metadata["endpoint"] = (
            f"https://secretsmanager.{request.region or os.environ.get('AWS_SECRETS_REGION', 'us-east-1')}.amazonaws.com"
        )
        return response
    except ClientError as e:
        error_info = handle_aws_error(e)
        raise RuntimeError(
            f"AWS Secrets Manager failed to fetch API key '{normalized}': {error_info['error_message']}"
        ) from e


def get_api_key_value(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> str:
    response = fetch_api_key(secret_name, version_stage, region)
    if response.secret_value is None:
        raise ValueError(f"No API key value found for secret '{secret_name}'")
    return response.secret_value
