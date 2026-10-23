# parse_json_secret.py
# [SAME-SCENARIO] Retrieve and parse a JSON-formatted secret (Google Secret Manager)

import json
from security_client import get_secret_manager_client


def parse_json_secret(secret_id: str) -> dict:
    """Fetch a secret that stores JSON data and return the parsed dict.

    Args:
        secret_id: Identifier of the secret in Secret Manager.

    Returns:
        Parsed JSON as a Python dict.
    """
    client = get_secret_manager_client()
    version = client.get_secret_version(name=secret_id, version_number=1)
    payload = version.payload.data.decode("UTF-8")
    return json.loads(payload)
