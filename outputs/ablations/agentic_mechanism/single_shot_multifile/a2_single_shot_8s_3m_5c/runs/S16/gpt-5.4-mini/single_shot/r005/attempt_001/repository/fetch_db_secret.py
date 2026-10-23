import json
from security_client import get_client, build_secret_path
from security_models import SecretResponse, normalize_db_secret


def fetch_db_secret(secret_name: str, version: str = "latest") -> dict:
    client = get_client()
    name = build_secret_path(secret_name, version)
    response = client.access_secret_version(name=name)
    payload = SecretResponse.from_google_secret_manager(response)
    data = normalize_db_secret(payload.as_text())
    return data
