"""
fetch_db_secret.py - Fetches a database connection secret at runtime.

Uses AWS Secrets Manager (boto3 SDK) to retrieve a database connection
secret that typically contains credentials, host, port, and database name
in a JSON-formatted secret value.

Provider: AWS Secrets Manager (secretsmanager.us-east-1.amazonaws.com)
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

from botocore.exceptions import ClientError

from security_client import (
    get_secrets_manager_client,
    resolve_secret_id,
    handle_aws_client_error,
    parse_get_secret_value_response,
    parse_json_secret_value,
)
from security_models import SecretResponse

logger = logging.getLogger(__name__)


@dataclass
class DatabaseCredentials:
    """Parsed database connection credentials from a secrets store."""
    host: str = ""
    port: int = 0
    username: str = ""
    password: str = ""
    dbname: str = ""
    engine: str = ""
    extra: Dict[str, str] = field(default_factory=dict)


def parse_db_credentials(secret_value: str) -> DatabaseCredentials:
    """
    Parse a JSON-formatted database secret value into structured credentials.

    Supports common AWS RDS/Database secret JSON schema:
    {
        "engine": "postgres",
        "host": "mydb.cluster-xyz.us-east-1.rds.amazonaws.com",
        "port": 5432,
        "username": "admin",
        "password": "supersecret",
        "dbname": "myapp"
    }
    """
    parsed = parse_json_secret_value(secret_value)
    return DatabaseCredentials(
        host=parsed.get("host", parsed.get("db_host", "")),
        port=int(parsed.get("port", 0)),
        username=parsed.get("username", parsed.get("db_user", "")),
        password=parsed.get("password", parsed.get("db_password", "")),
        dbname=parsed.get("dbname", parsed.get("database", "")),
        engine=parsed.get("engine", parsed.get("db_type", "")),
        extra={k: str(v) for k, v in parsed.items()
               if k not in ("host", "port", "username", "password", "dbname", "engine",
                            "db_host", "db_user", "db_password", "database", "db_type")},
    )


def fetch_db_secret(
    secret_id: str,
    version_stage: str = "AWSCURRENT",
) -> SecretResponse:
    """
    Fetch a database connection secret from AWS Secrets Manager.

    Args:
        secret_id: The secret name or ARN for the database credential.
        version_stage: The staging label for the secret version.

    Returns:
        SecretResponse with the raw secret value and parsed DB credentials
        attached as extra metadata.
    """
    resolved_id = resolve_secret_id(secret_id)
    client = get_secrets_manager_client()

    try:
        response = client.get_secret_value(
            SecretId=resolved_id,
            VersionStage=version_stage,
        )
        secret_response = parse_get_secret_value_response(response, resolved_id)

        if secret_response.success and secret_response.secret_value:
            db_creds = parse_db_credentials(secret_response.secret_value)
            secret_response.metadata = None
            secret_response.raw_response["parsed_credentials"] = {
                "host": db_creds.host,
                "port": db_creds.port,
                "username": db_creds.username,
                "engine": db_creds.engine,
                "dbname": db_creds.dbname,
            }
        return secret_response
    except ClientError as e:
        return handle_aws_client_error(e, resolved_id)
    except Exception as exc:
        logger.exception("Unexpected error fetching DB secret %s", resolved_id)
        return SecretResponse(
            success=False,
            secret_id=resolved_id,
            error_message=f"Unexpected error: {exc}",
        )


def fetch_db_credentials(
    secret_id: str,
    version_stage: str = "AWSCURRENT",
) -> Optional[DatabaseCredentials]:
    """
    Convenience function to fetch and parse database credentials.

    Returns a DatabaseCredentials object or None on failure.
    """
    result = fetch_db_secret(secret_id, version_stage)
    if result.success and result.secret_value:
        return parse_db_credentials(result.secret_value)
    logger.warning("Failed to fetch DB secret %s: %s", secret_id, result.error_message)
    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    secret_name = "prod/rds/myapp-db-credentials"
    creds = fetch_db_credentials(secret_name)
    if creds:
        print(f"DB host: {creds.host}:{creds.port}, engine: {creds.engine}")
    else:
        print("Failed to fetch database credentials")
