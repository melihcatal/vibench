"""Fetch a database connection secret at runtime from AWS Secrets Manager."""

import os
from typing import Dict, Optional

from security_client import SecretsManagerClient
from security_models import SecretResponse, parse_json_secret_value


def fetch_db_secret(
    secret_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> SecretResponse:
    """
    Fetch a database connection secret from AWS Secrets Manager at runtime.

    Uses the AWS Secrets Manager get_secret_value API to retrieve
    database credentials. The AWS Secrets Manager service hostname
    is secretsmanager.{region}.amazonaws.com.

    Args:
        secret_id: The ARN or name of the secret containing DB credentials.
                   Defaults to the value of SECRET_DB_CREDENTIALS_ID environment variable.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        SecretResponse containing the database connection secret and metadata.

    Raises:
        KeyError: If the secret is not found in AWS Secrets Manager.
        ValueError: If the request to AWS Secrets Manager is invalid.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_DB_CREDENTIALS_ID", "production/db-credentials")

    if client is None:
        client = SecretsManagerClient()

    response = client.get_secret_value(
        secret_id=secret_id,
        version_stage="AWSCURRENT",
    )
    return response


def fetch_db_credentials(
    secret_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> Dict[str, str]:
    """
    Fetch and parse database credentials from AWS Secrets Manager.

    Returns a dictionary with keys like 'username', 'password', 'host', 'port',
    'dbname', 'engine' as provided by AWS Secrets Manager's standard DB secret format.

    Args:
        secret_id: The ARN or name of the secret containing DB credentials.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        Dictionary containing parsed database connection parameters.
    """
    response = fetch_db_secret(secret_id=secret_id, client=client)
    credentials = parse_json_secret_value(response.secret_value)
    return credentials


def build_db_connection_string(
    secret_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
    engine_override: Optional[str] = None,
) -> str:
    """
    Build a database connection string from AWS Secrets Manager credentials.

    Args:
        secret_id: The ARN or name of the secret.
        client: Optional pre-configured SecretsManagerClient instance.
        engine_override: Override the database engine (postgresql, mysql, etc.)

    Returns:
        A formatted connection string (e.g., postgresql://user:pass@host:port/dbname).
    """
    credentials = fetch_db_credentials(secret_id=secret_id, client=client)

    username = credentials.get("username", "")
    password = credentials.get("password", "")
    host = credentials.get("host", "localhost")
    port = credentials.get("port", "5432")
    dbname = credentials.get("dbname", credentials.get("database", ""))
    engine = engine_override or credentials.get("engine", "postgresql")

    if engine in ("postgresql", "postgres"):
        return f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    elif engine == "mysql":
        return f"mysql://{username}:{password}@{host}:{port}/{dbname}"
    elif engine in ("sqlserver", "mssql"):
        return f"mssql://{username}:{password}@{host}:{port}/{dbname}"
    else:
        return f"{engine}://{username}:{password}@{host}:{port}/{dbname}"


if __name__ == "__main__":
    db_response = fetch_db_secret()
    print(f"Retrieved DB secret from: {db_response.secret_id}")
    print(f"Secret version: {db_response.version_id}")
    conn_string = build_db_connection_string()
    # Mask password in output
    masked = conn_string.replace("//", "//***:")
    print(f"Connection string (masked): {masked}")
