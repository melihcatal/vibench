from security_client import SecretManagerClient
import json


def parse_json_secret(secret_id: str) -> dict:
    client = SecretManagerClient()
    secret_value = client.get_secret_version(secret_id=secret_id)
    return json.loads(secret_value)
