"""
fetch_db_secret.py - Fetches a database connection secret at runtime from AWS Secrets Manager.

Provider: AWS Secrets Manager
SDK: boto3
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Service hostname: secretsmanager.<region>.amazonaws.com
"""

import os
import json
import logging
from typing import Optional, Dict, Any

from security_client import get_secrets_manager_client, retry_with_backoff, validate_secret_name
from security_models import SecretResponse, normalize_secret_response

logger = logging.getLogger(__name__)

# Well-known JSON keys for RDS/database secrets managed by AWS Secrets Manager
_DB_KEYS = ("username", "password", "host", "port", "dbname", "engine")


def fetch_db_secret(secret_name: Optional[str] = None) -> SecretResponse:
    """
    Retrieve a database connection secret from AWS Secrets Manager.

    This is typically used for RDS or other database credentials that
    are stored as JSON documents in Secrets Manager.

    Args:
        secret_name: Name of the database secret.
                     Defaults to the DB_SECRET_NAME env var.

    Returns:
        SecretResponse with the raw secret string containing DB credentials.

    Raises:
        ValueError: If the secret name is invalid.
        ClientError: On AWS API errors.
    """
    secret_name = secret_name or os.environ.get("DB_SECRET_NAME", "")
    if not validate_secret_name(secret_name):
        raise ValueError(f"Invalid or missing DB secret name: {secret_name!r}")

    client = get_secrets_manager_client()

    def _get_secret():
        return client.get_secret_value(SecretId=secret_name)

    raw_response = retry_with_backoff(_get_secret)
    secret_resp = normalize_secret_response(raw_response, secret_name)
    logger.info(
        "Fetched DB connection secret '%s' (version %s)",
        secret_name,
        secret_resp.version_id,
    )
    return secret_resp


def parse_db_credentials(secret_response: SecretResponse) -> Dict[str, Any]:
    """
    Parse the DB credential fields from a fetched secret.

    Returns a dict with keys like username, password, host, port, dbname, engine.
    Raises ValueError if the secret cannot be parsed as JSON or is missing required keys.
    """
    if secret_response.secret_string is None:
        raise ValueError("DB secret string is empty")

    try:
        creds = json.loads(secret_response.secret_string)
    except json.JSONDecodeError as exc:
        raise ValueError(f"DB secret is not valid JSON: {exc}") from exc

    for key in _DB_KEYS:
        if key not in creds:
            logger.warning("Expected DB credential key '%s' not found in secret", key)

    return creds


def get_db_connection_string(secret_name: Optional[str] = None) -> str:
    """
    Build a standard DB connection string (e.g. postgresql://user:pass@host:port/dbname)
    from the stored secret.
    """
    resp = fetch_db_secret(secret_name)
    creds = parse_db_credentials(resp)

    engine = creds.get("engine", "postgresql")
    user = creds.get("username", "")
    password = creds.get("password", "")
    host = creds.get("host", "")
    port = creds.get("port", 5432)
    dbname = creds.get("dbname", "")

    if engine in ("mysql", "mariadb"):
        scheme = "mysql"
    elif "postgres" in engine:
        scheme = "postgresql"
    else:
        scheme = engine

    return f"{scheme}://{user}:{password}@{host}:{port}/{dbname}"
