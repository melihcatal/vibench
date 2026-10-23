from typing import Dict, Any
from security_client import SecretManagerClient
from security_models import JsonSecret


def parse_json_secret(secret_id: str) -> Dict[str, Any]:
    """Retrieves and parses a JSON-formatted secret from Google Secret Manager."""
    client = SecretManagerClient()
    secret_payload = client.access_secret_version(secret_id)
    json_secret = JsonSecret.from_json_string(secret_id, secret_payload)
    return json_secret.json_data
