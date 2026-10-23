import os
import re
from security_client import fetch_secret, get_secrets_manager_client
from security_models import SecretRequest, SecretResponse


def fetch_db_secret(
    secret_id: str = None, version_stage: str = "AWSCURRENT"
) -> SecretResponse:
    target_id = secret_id or os.environ.get("DB_SECRET_ID", "prod/database/primary")
    request = SecretRequest(
        secret_id=target_id,
        version_stage=version_stage,
        with_decryption=True,
    )
    return fetch_secret(request)


def build_connection_string(secret_id: str = None) -> str:
    response = fetch_db_secret(secret_id)
    creds = response.secret_value
    if isinstance(creds, str):
        import json

        creds = json.loads(creds)
    engine = creds.get("engine", "postgresql")
    host = creds.get("host", "localhost")
    port = creds.get("port", 5432)
    dbname = creds.get("dbname", creds.get("database", "appdb"))
    username = creds.get("username", creds.get("user", "admin"))
    password = creds.get("password", "")
    if engine in ("postgres", "postgresql"):
        return f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    elif engine == "mysql":
        return f"mysql://{username}:{password}@{host}:{port}/{dbname}"
    elif engine == "oracle":
        return f"oracle://{username}:{password}@{host}:{port}/{dbname}"
    return f"{engine}://{username}:{password}@{host}:{port}/{dbname}"


def extract_db_credentials(secret_id: str = None) -> dict:
    response = fetch_db_secret(secret_id)
    creds = response.secret_value
    if isinstance(creds, str):
        import json

        creds = json.loads(creds)
    return {
        "host": creds.get("host", ""),
        "port": creds.get("port", 5432),
        "username": creds.get("username", creds.get("user", "")),
        "password": creds.get("password", ""),
        "database": creds.get("dbname", creds.get("database", "")),
        "engine": creds.get("engine", "postgresql"),
    }


if __name__ == "__main__":
    conn_str = build_connection_string()
    print(f"Connection string: {conn_str}")
