import os

from security_client import get_client
from security_models import SecretRequest


def fetch_api_key(secret_name: str | None = None) -> str:
    client = get_client()
    request = SecretRequest(
        name=secret_name or os.getenv("API_KEY_SECRET_NAME", "api_key")
    )
    return str(client.get_secret(request).value)
