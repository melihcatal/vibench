import boto3
from security_client import get_secret_manager_client, resolve_secret_name
from security_models import SecretFetchRequest, normalize_connection_secret


def fetch_db_secret() -> dict:
    request = SecretFetchRequest(secret_id=resolve_secret_name("DB_SECRET_ID", "database/connection"))
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=request.secret_id)
    payload = response.get("SecretString") or response.get("SecretBinary", b"").decode("utf-8")
    return normalize_connection_secret(payload)
