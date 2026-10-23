import json

from security_client import load_secret_name, secrets_manager_client
from security_models import normalize_secret_payload, parse_json_secret


def fetch_and_parse_json_secret(secret_name: str = None):
    client = secrets_manager_client()
    secret_id = secret_name or load_secret_name("app/config/json")
    response = client.get_secret_value(SecretId=secret_id)
    normalized = normalize_secret_payload(response)
    return parse_json_secret(normalized["value"])
