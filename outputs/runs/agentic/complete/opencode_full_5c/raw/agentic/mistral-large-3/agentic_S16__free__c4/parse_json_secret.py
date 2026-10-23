import json
import os
from security_client import GoogleSecretManagerClient


def parse_json_secret(secret_id: str = "JSON_SECRET") -> dict:
    client = GoogleSecretManagerClient()
    secret_payload = client.get_secret(secret_id)
    try:
        return json.loads(secret_payload)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON secret {secret_id}: {str(e)}")
