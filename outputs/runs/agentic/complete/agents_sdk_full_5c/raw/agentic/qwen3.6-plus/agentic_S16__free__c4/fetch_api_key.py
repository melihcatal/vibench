"""Fetch an API key from AWS Secrets Manager."""

import os
import json
import boto3
from botocore.exceptions import ClientError
from security_client import get_secrets_client
from security_models import SecretFetchResult, SecretError


def fetch_api_key(secret_id: str, region: str = None) -> SecretFetchResult:
    """Fetch an API key from AWS Secrets Manager.

    Args:
        secret_id: The name or ARN of the secret in AWS Secrets Manager.
        region: AWS region override; falls back to AWS_DEFAULT_REGION or us-east-1.

    Returns:
        SecretFetchResult with the retrieved API key string.
    """
    try:
        client = get_secrets_client(region=region)
        response = client.get_secret_value(SecretId=secret_id)
        secret_value = response.get("SecretString", "")
        return SecretFetchResult(
            secret_id=secret_id,
            secret_value=secret_value,
            version_id=response.get("VersionId", ""),
            provider="aws_secrets_manager",
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        raise SecretError(
            secret_id=secret_id,
            message=f"AWS Secrets Manager error: {error_code}",
            error_code=error_code,
        )


def fetch_api_key_as_dict(secret_id: str, region: str = None) -> dict:
    """Fetch an API key secret and return it as a parsed dictionary.

    Assumes the secret stored in AWS Secrets Manager is a JSON string.
    """
    result = fetch_api_key(secret_id, region=region)
    try:
        return json.loads(result.secret_value)
    except (json.JSONDecodeError, AttributeError):
        return {"raw_api_key": result.secret_value}


if __name__ == "__main__":
    secret_id = os.environ.get("API_KEY_SECRET_ID", "prod/api/service-key")
    result = fetch_api_key(secret_id)
    print(f"Retrieved key version: {result.version_id}")
