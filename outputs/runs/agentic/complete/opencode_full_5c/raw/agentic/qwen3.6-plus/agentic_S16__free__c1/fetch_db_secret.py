import os
from botocore.exceptions import ClientError

from security_models import SecretRequest, SecretResponse, SecretType
from security_client import (
    fetch_secret_value,
    handle_aws_error,
    normalize_secret_name,
)


def fetch_db_secret(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> SecretResponse:
    normalized = normalize_secret_name(secret_name)
    request = SecretRequest(
        secret_name=normalized,
        version_stage=version_stage,
        region=region,
        secret_type=SecretType.DATABASE,
    )

    try:
        response = fetch_secret_value(
            secret_name=request.secret_name,
            version_stage=request.version_stage,
            region=request.region,
        )
        response.metadata["secret_type"] = SecretType.DATABASE.value
        response.metadata["provider"] = "aws_secrets_manager"
        response.metadata["endpoint"] = (
            f"https://secretsmanager.{request.region or os.environ.get('AWS_SECRETS_REGION', 'us-east-1')}.amazonaws.com"
        )
        return response
    except ClientError as e:
        error_info = handle_aws_error(e)
        raise RuntimeError(
            f"AWS Secrets Manager failed to fetch DB secret '{normalized}': {error_info['error_message']}"
        ) from e


def parse_db_connection_string(secret_value: str) -> dict:
    try:
        import json

        parsed = json.loads(secret_value)
    except (json.JSONDecodeError, TypeError):
        parts = secret_value.split("://", 1)
        if len(parts) == 2:
            scheme, rest = parts
            return {"connection_string": secret_value, "scheme": scheme}
        return {"connection_string": secret_value}

    connection_info = {
        "host": parsed.get("host", ""),
        "port": parsed.get("port", 5432),
        "username": parsed.get("username", ""),
        "password": parsed.get("password", ""),
        "dbname": parsed.get("dbname", parsed.get("database", "")),
        "engine": parsed.get("engine", ""),
    }
    return connection_info


def get_db_connection_info(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> dict:
    response = fetch_db_secret(secret_name, version_stage, region)
    if response.secret_value is None:
        raise ValueError(f"No DB secret value found for '{secret_name}'")
    return parse_db_connection_string(response.secret_value)
