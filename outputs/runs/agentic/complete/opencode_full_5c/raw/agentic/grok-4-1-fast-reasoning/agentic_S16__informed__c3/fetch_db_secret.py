import json
from security_client import fetch_secret
from security_models import SecretRequest


def fetch_db_secret(secret_name: str = "db-connection") -> dict:
    resp = fetch_secret(SecretRequest(name=secret_name))
    if not resp.secret_string:
        raise ValueError("Secret string is empty")
    return json.loads(resp.secret_string)
