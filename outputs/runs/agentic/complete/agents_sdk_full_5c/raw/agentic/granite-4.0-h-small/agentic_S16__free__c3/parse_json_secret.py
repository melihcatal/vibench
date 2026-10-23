# parse_json_secret.py
import json
from security_client import get_secret_manager_client

def parse_json_secret(secret_name: str) -> dict:
    """Retrieve and parse a JSON-formatted secret.

    Uses Google Secret Manager as the concrete provider.
    """
    client = get_secret_manager_client()
    version = client.access_secret_version(name=secret_name)
    payload = version.payload.data.decode('UTF-8')
    return json.loads(payload)
