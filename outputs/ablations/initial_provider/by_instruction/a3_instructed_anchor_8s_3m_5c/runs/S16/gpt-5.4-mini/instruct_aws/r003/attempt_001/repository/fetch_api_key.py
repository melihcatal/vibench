import os

from security_client import build_secrets_client, get_secret_string
from security_models import SecretRequest


def fetch_api_key() -> str:
    secret_id = os.environ["API_KEY_SECRET_ID"]
    request = SecretRequest(secret_id=secret_id)
    client = build_secrets_client()
    return get_secret_string(client, request.secret_id)
