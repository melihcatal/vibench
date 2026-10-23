"""
fetch_db_secret.py - Fetches a database connection secret at runtime from AWS Secrets Manager.

Retrieves database credentials (host, port, username, password, dbname) stored
in secretsmanager.amazonaws.com and returns them parsed for runtime use.
"""

from __future__ import annotations

import json
import logging
from typing import Optional, Dict, Any

from security_client import get_secretsmanager_client, get_secret_value
from security_models import SecretResponse, describe_secret

logger = logging.getLogger(__name__)


def fetch_db_secret(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch a database connection secret from AWS Secrets Manager.

    Expects the secret to be JSON-formatted with keys:
    host, port, username, password, dbname (and optionally engine, ssl).

    Args:
        secret_name: The name or ARN of the DB secret.
        version_stage: The version stage to retrieve.
        region: AWS region override.

    Returns:
        Dict with parsed database connection parameters.
    """
    client = get_secretsmanager_client(region_name=region)
    logger.info("Fetching DB secret from AWS Secrets Manager: %s", secret_name)

    secret_value_resp = get_secret_value(
        client,
        secret_id=secret_name,
        version_stage=version_stage,
    )

    metadata = describe_secret(client, secret_name)

    secret_response = SecretResponse.from_aws_response(secret_value_resp, metadata)
    db_config = json.loads(secret_response.value)

    connection_info = {
        "host": db_config.get("host"),
        "port": db_config.get("port"),
        "username": db_config.get("username"),
        "password": db_config.get("password"),
        "dbname": db_config.get("dbname"),
        "engine": db_config.get("engine", "postgres"),
        "ssl": db_config.get("ssl", True),
        "secret_arn": metadata.get("ARN", ""),
        "version_id": secret_response.version_id,
    }

    logger.info("Retrieved DB secret for host=%s, engine=%s", connection_info["host"], connection_info["engine"])
    return connection_info


def build_connection_string(db_config: Dict[str, Any]) -> str:
    """
    Build a database connection string from the fetched config.

    Args:
        db_config: Dict from fetch_db_secret().

    Returns:
        Formatted connection string (PostgreSQL style).
    """
    engine = db_config.get("engine", "postgres")
    return (
        f"{engine}://{db_config['username']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db_secret_name = "production/db/postgres-main"
    config = fetch_db_secret(db_secret_name)
    conn_str = build_connection_string(config)
    logger.info("Built connection string for %s", config["host"])
    print(f"DB engine: {config['engine']}")
    print(f"Host: {config['host']}")
    print(f"Port: {config['port']}")
