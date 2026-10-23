import json
from security_client import SecretClientWrapper


def parse_json_secret(secret_name: str) -> dict:
    """Retrieves and parses a JSON‑formatted secret stored in the secret manager.
    Returns the deserialized JSON object (dict/list).
    """
    client = SecretClientWrapper()
    response = client.get_secret(secret_name)
    # Ensure the secret value is a JSON string before parsing
    secret_str = response.value
    return json.loads(secret_str)
