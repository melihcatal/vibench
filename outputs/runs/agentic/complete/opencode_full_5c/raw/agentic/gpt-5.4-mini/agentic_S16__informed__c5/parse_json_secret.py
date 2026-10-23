import os

from security_client import build_secrets_client, default_secret_id
from security_models import decode_secret_payload


def parse_json_secret(secret_name: str = None) -> dict:
    client = build_secrets_client()
    secret_id = default_secret_id(
        secret_name or os.getenv("JSON_SECRET_NAME", "json-secret")
    )
    response = client.get_secret_value(SecretId=secret_id)
    secret = decode_secret_payload(
        response.get("SecretString") or response.get("SecretBinary")
    )
    return secret if isinstance(secret, dict) else {"value": secret}
