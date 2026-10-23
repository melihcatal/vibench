import json
from security_client import SecretClient

def parse_json_secret(secret_id: str) -> dict:
    """Retrieve a secret that stores JSON data and return it as a Python dict.

    Uses Azure Key Vault as the concrete provider.
    The secret identifier is passed in and the service returns a JSON string.
    """
    client = SecretClient()
    json_str = client.get_secret(secret_id)
    return json.loads(json_str)