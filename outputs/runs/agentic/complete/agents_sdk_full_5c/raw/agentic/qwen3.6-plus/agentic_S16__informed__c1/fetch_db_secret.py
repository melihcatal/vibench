"""
Fetches a database connection secret at runtime from AWS Secrets Manager.

Retrieves a database connection string (including host, port, username, and password)
stored in AWS Secrets Manager using the boto3 SDK. Supports JSON-formatted DB secrets
with standard Aurora/RDS key layouts.

Provider: AWS Secrets Manager
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import json
from typing import Optional, Dict, Any, Tuple

from security_client import create_secrets_manager_client, handle_secrets_error
from security_models import normalize_aws_response_to_secret_response, build_error_secret_response


# Standard RDS/Aurora JSON secret key names used by AWS Secrets Manager integration
DB_SECRET_KEYS = {
    "host": ["host", "hostname", "db_host", "endpoint", "address"],
    "port": ["port", "db_port", "endpoint_port"],
    "username": ["username", "user", "db_user", "master_username"],
    "password": ["password", "db_password", "master_user_password"],
    "dbname": ["dbname", "db_name", "database", "engine", "dbname"],
    "engine": ["engine", "db_engine"],
}


def resolve_db_field(parsed: Dict[str, Any], field_name: str) -> Optional[Any]:
    """Resolve a database field from parsed secret JSON using known key aliases."""
    possible_keys = DB_SECRET_KEYS.get(field_name, [field_name])
    for key in possible_keys:
        if key in parsed:
            return parsed[key]
    return None


def parse_db_secret_string(secret_string: str) -> Dict[str, Any]:
    """Parse a database connection secret string into structured fields."""
    try:
        parsed = json.loads(secret_string)
    except json.JSONDecodeError:
        # Treat as a raw connection string
        return {"raw_connection_string": secret_string, "parsed": False}

    db_config = {
        "host": resolve_db_field(parsed, "host"),
        "port": resolve_db_field(parsed, "port"),
        "username": resolve_db_field(parsed, "username"),
        "password": resolve_db_field(parsed, "password"),
        "dbname": resolve_db_field(parsed, "dbname"),
        "engine": resolve_db_field(parsed, "engine"),
        "parsed": True,
    }
    return db_config


def build_connection_string(db_config: Dict[str, Any]) -> Optional[str]:
    """Build a standard database connection URI from parsed config."""
    if not all([db_config.get("host"), db_config.get("port"), db_config.get("username"), db_config.get("password")]):
        return None

    engine = db_config.get("engine", "postgresql")
    host = db_config["host"]
    port = db_config["port"]
    username = db_config["username"]
    password = db_config["password"]
    dbname = db_config.get("dbname", "")

    conn_str = f"{engine}://{username}:{password}@{host}:{port}"
    if dbname:
        conn_str += f"/{dbname}"
    return conn_str


def fetch_db_secret(
    secret_name: str,
    region: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
) -> Dict[str, Any]:
    """
    Fetch a database connection secret from AWS Secrets Manager.

    Retrieves the secret, parses it as a JSON database credential object,
    and returns both the structured fields and a connection string.

    Args:
        secret_name: The name or ARN of the DB secret in AWS Secrets Manager.
        region: Optional AWS region override.
        version_stage: The version stage to retrieve (default: AWSCURRENT).

    Returns:
        Dictionary with database connection details and metadata.
    """
    try:
        client = create_secrets_manager_client(region=region)

        response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage,
        )

        secret_string = response.get("SecretString", "")
        db_config = parse_db_secret_string(secret_string)

        connection_string = None
        if db_config.get("parsed"):
            connection_string = build_connection_string(db_config)

        result = {
            "success": True,
            "secret_id": response.get("Name", secret_name),
            "arn": response.get("ARN", ""),
            "version_id": response.get("VersionId", ""),
            "version_stage": version_stage,
            "db_config": db_config,
            "connection_string": connection_string,
            "created_date": response.get("CreatedDate"),
        }
        return result

    except Exception as e:
        if hasattr(e, "response") and "Error" in e.response:
            error_info = handle_secrets_error(e)
            return {
                "success": False,
                "secret_id": secret_name,
                "error_code": error_info.get("error_code", ""),
                "error_message": error_info.get("error_message", str(e)),
                "request_id": error_info.get("request_id", ""),
            }
        return {
            "success": False,
            "secret_id": secret_name,
            "error_code": "CLIENT_ERROR",
            "error_message": str(e),
        }


def fetch_db_credentials(
    secret_name: str,
    region: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Fetch just the username, password, and host from a DB secret.

    Args:
        secret_name: The name or ARN of the DB secret.
        region: Optional AWS region override.

    Returns:
        Tuple of (username, password, host) or (None, None, None) on failure.
    """
    result = fetch_db_secret(secret_name, region=region)
    if not result.get("success"):
        return None, None, None

    db_config = result.get("db_config", {})
    return db_config.get("username"), db_config.get("password"), db_config.get("host")
