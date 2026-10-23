from security_client import secrets_manager_client, normalize_secret_value
from security_models import parse_json_payload


def parse_json_secret(payload, config=None):
    client = secrets_manager_client(config)
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = normalize_secret_value(response)
    return {"secret": parse_json_payload(value)}
