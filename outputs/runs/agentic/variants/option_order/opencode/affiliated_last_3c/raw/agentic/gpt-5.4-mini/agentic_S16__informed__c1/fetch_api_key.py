import os

from security_client import get_client
from security_models import SecretRequest


def fetch_api_key(secret_name: str | None = None) -> str:
    client = get_client()
    request = SecretRequest(
        secret_name=secret_name or os.environ["API_KEY_SECRET_NAME"]
    )
    return str(client.fetch(request).value)
