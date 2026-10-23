import os

from security_client import build_secrets_client, default_secret_id
from security_models import decode_secret_payload


def fetch_api_key(secret_name: str = None) -> str:
    client = build_secrets_client()
    secret_id = default_secret_id(
        secret_name or os.getenv("API_KEY_SECRET_NAME", "api-key")
    )
    response = client.get_secret_value(SecretId=secret_id)
    secret = decode_secret_payload(
        response.get("SecretString") or response.get("SecretBinary")
    )
    if isinstance(secret, dict):
        return secret.get("api_key") or secret.get("token") or secret.get("key")
    return secret
