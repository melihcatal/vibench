"""Retrieve and parse a JSON-formatted secret from AWS Secrets Manager."""

import os
import json
import boto3
from botocore.exceptions import ClientError
from security_client import get_secrets_client
from security_models import SecretFetchResult, SecretError


def parse_json_secret(secret_id: str, region: str = None) -> dict:
    """Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_id: The name or ARN of the secret in AWS Secrets Manager.
        region: AWS region override.

    Returns:
        Parsed dictionary from the JSON secret value.

    Raises:
        SecretError: If the secret cannot be retrieved or is not valid JSON.
    """
    try:
        client = get_secrets_client(region=region)
        response = client.get_secret_value(SecretId=secret_id)
        secret_string = response.get("SecretString", "")
        if not secret_string:
            raise SecretError(
                secret_id=secret_id,
                message="Secret value is empty",
                error_code="EMPTY_SECRET",
            )
        parsed = json.loads(secret_string)
        return parsed
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        raise SecretError(
            secret_id=secret_id,
            message=f"AWS Secrets Manager error: {error_code}",
            error_code=error_code,
        )
    except json.JSONDecodeError as exc:
        raise SecretError(
            secret_id=secret_id,
            message=f"Secret is not valid JSON: {exc}",
            error_code="INVALID_JSON",
        )


def parse_json_secret_with_metadata(secret_id: str, region: str = None) -> dict:
    """Retrieve JSON secret and include AWS Secrets Manager metadata.

    Returns a dict with:
        - secret_data: the parsed JSON payload
        - version_id: the version ID from AWS Secrets Manager
        - arn: the secret ARN
        - created_date: when this version was created
    """
    try:
        client = get_secrets_client(region=region)
        response = client.get_secret_value(SecretId=secret_id)
        secret_string = response.get("SecretString", "")
        parsed = json.loads(secret_string)
        return {
            "secret_data": parsed,
            "version_id": response.get("VersionId", ""),
            "arn": response.get("ARN", ""),
            "created_date": str(response.get("CreatedDate", "")),
            "provider": "aws_secrets_manager",
        }
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        raise SecretError(
            secret_id=secret_id,
            message=f"AWS Secrets Manager error: {error_code}",
            error_code=error_code,
        )


if __name__ == "__main__":
    secret_id = os.environ.get("JSON_SECRET_ID", "prod/config/service-config")
    data = parse_json_secret(secret_id)
    print(f"Parsed JSON secret with {len(data)} keys from AWS Secrets Manager")
