import json
from security_client import fetch_secret
from security_models import SecretRequest


def parse_json_secret(secret_name: str = "json-config") -> dict:
    resp = fetch_secret(SecretRequest(name=secret_name))
    if not resp.secret_string:
        raise ValueError("Secret string is empty")
    try:
        return json.loads(resp.secret_string)
    except json.JSONDecodeError:
        raise ValueError("Secret is not valid JSON")
