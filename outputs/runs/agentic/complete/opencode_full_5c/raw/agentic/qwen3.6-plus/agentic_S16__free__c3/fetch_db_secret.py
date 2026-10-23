from typing import Optional
from security_models import SecretRequest, SecretType
from security_client import get_vault_client


def fetch_db_secret(secret_path: str, mount_point: Optional[str] = None) -> dict:
    client = get_vault_client()
    try:
        request = SecretRequest(
            secret_path=secret_path,
            secret_type=SecretType.DATABASE,
            mount_point=mount_point,
        )
        response = client.read_secret(request)
        return response.value
    finally:
        client.close()


def build_connection_string(secret_path: str, mount_point: Optional[str] = None) -> str:
    secret = fetch_db_secret(secret_path, mount_point)
    host = secret.get("host", "")
    port = secret.get("port", 5432)
    dbname = secret.get("dbname", "")
    username = secret.get("username", "")
    password = secret.get("password", "")
    return f"postgresql://{username}:{password}@{host}:{port}/{dbname}"


if __name__ == "__main__":
    import os

    secret_path = os.environ.get("DB_SECRET_PATH", "prod/database/postgres-primary")
    conn_str = build_connection_string(secret_path)
    print(conn_str)
