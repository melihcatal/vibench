"""Retrieve and parse a JSON-formatted secret from AWS Secrets Manager."""

import os
import json
import boto3
from botocore.exceptions import ClientError

from security_client import get_secret_manager_client, resolve_secret_name
from security_models import SecretFetchRequest, SecretFetchResponse


def parse_json_secret(secret_name: str | None = None) -> SecretFetchResponse:
    """Fetch a JSON-formatted secret from AWS Secrets Manager and parse it.

    Provider: AWS Secrets Manager (boto3)
    Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    """
    target_name = resolve_secret_name(secret_name, default_env="JSON_SECRET_NAME")
    client = get_secret_manager_client()

    try:
        response = client.get_secret_value(SecretId=target_name)
        secret_string = response["SecretString"]

        parsed = json.loads(secret_string)

        return SecretFetchResponse(
            secret_name=target_name,
            secret_value=secret_string,
            version_id=response.get("VersionId"),
            metadata={
                "parsed_keys": list(parsed.keys()) if isinstance(parsed, dict) else None,
                "parsed_data": parsed,
                "secret_type": "json",
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
    except json.JSONDecodeError as exc:
        return SecretFetchResponse(
            secret_name=target_name,
            secret_value=None,
            error=f"JSON parsing failed: {exc}",
            provider="aws_secrets_manager",
        )


if __name__ == "__main__":
    result = parse_json_secret()
    if result.error:
        print(f"Error: {result.error}")
    else:
        meta = result.metadata or {}
        print(f"JSON secret retrieved from {result.secret_name}")
        print(f"Keys found: {meta.get('parsed_keys', [])}")
