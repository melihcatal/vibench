import json
from security_client import get_client, build_secret_path
from security_models import SecretResponse


def fetch_api_key(secret_name: str, version: str = "latest") -> str:
    client = get_client()
    name = build_secret_path(secret_name, version)
    response = client.access_secret_version(name=name)
    payload = SecretResponse.from_google_secret_manager(response)
    data = payload.as_text().strip()
    if not data:
        raise ValueError("empty secret payload")
    return data
