import os
import json
import logging
from typing import Optional
from urllib.parse import urlparse

from security_models import SecretRequest, SecretResponse
from security_client import fetch_secret_value, get_secrets_manager_client

logger = logging.getLogger(__name__)

AWS_SECRETS_MANAGER_SERVICE = "secretsmanager"
AWS_ENDPOINT_HOST = "secretsmanager.us-east-1.amazonaws.com"


def fetch_db_secret(
    secret_id: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
) -> SecretResponse:
    target_secret_id = secret_id or os.environ.get(
        "DB_SECRET_ID", "prod/database/postgres-connection"
    )

    request = SecretRequest(
        secret_id=target_secret_id,
        version_stage=version_stage,
        region=region,
    )

    response = fetch_secret_value(request)

    logger.info(
        "Fetched DB connection secret from AWS Secrets Manager: secret_id=%s, version=%s, endpoint=%s",
        response.secret_id,
        response.version_id,
        AWS_ENDPOINT_HOST,
    )

    return response


def parse_db_connection_string(
    secret_id: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
) -> dict:
    response = fetch_db_secret(secret_id, version_stage, region)
    secret_value = response.secret_value

    try:
        parsed = json.loads(secret_value)
        connection_parts = []

        engine = parsed.get("engine", "postgres")
        username = parsed.get("username", "")
        password = parsed.get("password", "")
        host = parsed.get("host", "")
        port = parsed.get("port", 5432)
        dbname = parsed.get("dbname", parsed.get("database", ""))

        connection_string = f"{engine}://{username}:{password}@{host}:{port}/{dbname}"

        return {
            "connection_string": connection_string,
            "engine": engine,
            "host": host,
            "port": port,
            "username": username,
            "database": dbname,
            "secret_version": response.version_id,
        }
    except json.JSONDecodeError:
        if secret_value.startswith(("postgres://", "mysql://", "mongodb://")):
            parsed_url = urlparse(secret_value)
            return {
                "connection_string": secret_value,
                "engine": parsed_url.scheme,
                "host": parsed_url.hostname or "",
                "port": parsed_url.port or 0,
                "username": parsed_url.username or "",
                "database": parsed_url.path.lstrip("/"),
                "secret_version": response.version_id,
            }
        return {
            "connection_string": secret_value,
            "raw": True,
            "secret_version": response.version_id,
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = parse_db_connection_string()
    print(json.dumps(result, indent=2))
