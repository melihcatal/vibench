import os
import json
from security_client import build_secret_request, fetch_secret
from security_models import SecretResponse


def fetch_db_secret(secret_name: str = None, region: str = None) -> SecretResponse:
    db_secret_name = secret_name or os.environ.get(
        "DB_SECRET_NAME", "prod/database/connection"
    )
    request = build_secret_request(
        secret_name=db_secret_name,
        version_stage="AWSCURRENT",
        region=region,
    )
    return fetch_secret(request)


def get_db_credentials(secret_name: str = None, region: str = None) -> dict:
    response = fetch_db_secret(secret_name, region)
    return json.loads(response.secret_value)


def get_db_connection_string(secret_name: str = None, region: str = None) -> str:
    creds = get_db_credentials(secret_name, region)
    host = creds.get("host", "")
    port = creds.get("port", 5432)
    dbname = creds.get("dbname", "")
    username = creds.get("username", "")
    password = creds.get("password", "")
    engine = creds.get("engine", "postgresql")
    return f"{engine}://{username}:{password}@{host}:{port}/{dbname}"
