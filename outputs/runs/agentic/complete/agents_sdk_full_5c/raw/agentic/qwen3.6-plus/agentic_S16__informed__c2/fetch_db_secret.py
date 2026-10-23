"""Fetch a database connection secret from AWS Secrets Manager at runtime."""

import os
import json
import boto3
from botocore.exceptions import ClientError

from security_client import get_secret_manager_client, resolve_secret_name
from security_models import SecretFetchRequest, SecretFetchResponse


def fetch_db_secret(secret_name: str | None = None) -> SecretFetchResponse:
    """Retrieve a database connection string secret from AWS Secrets Manager.

    Provider: AWS Secrets Manager (boto3)
    Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    """
    target_name = resolve_secret_name(secret_name, default_env="DB_SECRET_NAME")
    client = get_secret_manager_client()

    try:
        response = client.get_secret_value(SecretId=target_name)
        secret_value = response["SecretString"]

        parsed = _extract_connection_info(secret_value)
        return SecretFetchResponse(
            secret_name=target_name,
            secret_value=secret_value,
            version_id=response.get("VersionId"),
            metadata=parsed,
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


def _extract_connection_info(secret_string: str) -> dict:
    """Parse database connection fields from the secret payload."""
    try:
        data = json.loads(secret_string)
        host = data.get("host", "")
        port = data.get("port", 5432)
        dbname = data.get("dbname", data.get("database", ""))
        username = data.get("username", "")
        return {
            "host": host,
            "port": port,
            "dbname": dbname,
            "username": username,
            "connection_string": f"postgresql://{username}@{host}:{port}/{dbname}",
        }
    except json.JSONDecodeError:
        return {"raw_value": secret_string}


if __name__ == "__main__":
    result = fetch_db_secret()
    if result.error:
        print(f"Error: {result.error}")
    else:
        meta = result.metadata or {}
        print(f"DB secret retrieved from {result.secret_name}")
        print(f"Connection: {meta.get('connection_string', 'N/A')}")
