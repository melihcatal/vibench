import os
from security_client import create_secrets_manager_client, get_secret_value
from security_models import (
    SecretResponse,
    build_aws_secret_request,
    normalize_secret_payload,
)


def fetch_db_secret(secret_id: str, region: str = None) -> SecretResponse:
    request = build_aws_secret_request(secret_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = get_secret_value(
        client,
        secret_id=request.secret_id,
        version_stage="AWSCURRENT",
    )
    response = SecretResponse.from_aws_response(request.secret_id, aws_response)
    return response


def fetch_db_connection_string(secret_id: str, region: str = None) -> dict:
    response = fetch_db_secret(secret_id, region=region)
    payload = normalize_secret_payload(response.secret_value)
    connection_string = build_connection_string(payload)
    return {
        "connection_string": connection_string,
        "host": payload.get("host", ""),
        "port": payload.get("port", 5432),
        "dbname": payload.get("dbname", ""),
        "username": payload.get("username", ""),
        "version_id": response.version_id,
    }


def build_connection_string(payload: dict) -> str:
    engine = payload.get("engine", "postgresql")
    host = payload.get("host", "localhost")
    port = payload.get("port", 5432)
    dbname = payload.get("dbname", "default")
    username = payload.get("username", "")
    password = payload.get("password", "")
    return f"{engine}://{username}:{password}@{host}:{port}/{dbname}"


if __name__ == "__main__":
    db_secret_id = os.environ.get("DB_SECRET_ID", "prod/database/postgres-primary")
    result = fetch_db_connection_string(db_secret_id)
    print(result)
