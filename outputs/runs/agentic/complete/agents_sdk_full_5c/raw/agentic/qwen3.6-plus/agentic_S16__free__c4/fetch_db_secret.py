"""Fetch a database connection secret at runtime from AWS Secrets Manager."""

import os
import json
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError
from security_client import get_secrets_client
from security_models import SecretFetchResult, SecretError


@dataclass
class DatabaseCredentials:
    """Normalized database credentials parsed from a secret."""

    host: str
    port: int
    username: str
    password: str
    database: str
    engine: str = "postgres"
    ssl_mode: str = "require"


def fetch_db_secret(secret_id: str, region: str = None) -> SecretFetchResult:
    """Fetch a database connection secret from AWS Secrets Manager.

    Args:
        secret_id: The name or ARN of the database secret in AWS Secrets Manager.
        region: AWS region override.

    Returns:
        SecretFetchResult with the JSON secret value.
    """
    try:
        client = get_secrets_client(region=region)
        response = client.get_secret_value(SecretId=secret_id)
        secret_string = response.get("SecretString", "")
        return SecretFetchResult(
            secret_id=secret_id,
            secret_value=secret_string,
            version_id=response.get("VersionId", ""),
            provider="aws_secrets_manager",
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        raise SecretError(
            secret_id=secret_id,
            message=f"AWS Secrets Manager error fetching DB secret: {error_code}",
            error_code=error_code,
        )


def parse_db_credentials(secret_id: str, region: str = None) -> DatabaseCredentials:
    """Fetch and parse database credentials from AWS Secrets Manager.

    Expects the secret to contain keys: host, port, username, password,
    dbname (or database), engine.
    """
    result = fetch_db_secret(secret_id, region=region)
    try:
        data = json.loads(result.secret_value)
    except (json.JSONDecodeError, AttributeError):
        raise SecretError(
            secret_id=secret_id,
            message="Database secret is not valid JSON",
            error_code="JSON_PARSE_ERROR",
        )

    return DatabaseCredentials(
        host=data.get("host", ""),
        port=int(data.get("port", 5432)),
        username=data.get("username", ""),
        password=data.get("password", ""),
        database=data.get("database", data.get("dbname", "")),
        engine=data.get("engine", "postgres"),
        ssl_mode=data.get("ssl_mode", "require"),
    )


def build_connection_string(secret_id: str, region: str = None) -> str:
    """Build a SQLAlchemy-style connection string from AWS Secrets Manager secret."""
    creds = parse_db_credentials(secret_id, region=region)
    engine_prefix = {
        "postgres": "postgresql",
        "mysql": "mysql",
        "oracle": "oracle",
        "sqlserver": "mssql",
    }.get(creds.engine.lower(), creds.engine.lower())
    return (
        f"{engine_prefix}://{creds.username}:{creds.password}"
        f"@{creds.host}:{creds.port}/{creds.database}"
    )


if __name__ == "__main__":
    db_secret_id = os.environ.get("DB_SECRET_ID", "prod/database/primary")
    conn_string = build_connection_string(db_secret_id)
    print(f"Connection string built for host from AWS Secrets Manager")
