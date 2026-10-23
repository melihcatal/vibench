"""Fetch an API key from AWS Secrets Manager at runtime."""

import os
import boto3
from botocore.exceptions import ClientError

from security_client import get_secret_manager_client, resolve_secret_name
from security_models import SecretFetchRequest, SecretFetchResponse


def fetch_api_key(secret_name: str | None = None) -> SecretFetchResponse:
    """Retrieve an API key secret from AWS Secrets Manager.

    Provider: AWS Secrets Manager (boto3)
    Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    """
    target_name = resolve_secret_name(secret_name, default_env="API_KEY_SECRET_NAME")
    client = get_secret_manager_client()

    try:
        response = client.get_secret_value(SecretId=target_name)
        secret_value = response["SecretString"]
        return SecretFetchResponse(
            secret_name=target_name,
            secret_value=secret_value,
            version_id=response.get("VersionId"),
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


if __name__ == "__main__":
    result = fetch_api_key()
    if result.error:
        print(f"Error: {result.error}")
    else:
        print(f"API key retrieved from {result.secret_name} (version {result.version_id})")
        print(f"Value length: {len(result.secret_value)}")
