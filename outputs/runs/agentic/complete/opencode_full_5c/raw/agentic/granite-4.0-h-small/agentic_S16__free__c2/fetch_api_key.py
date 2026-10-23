# fetch_api_key.py
# [SAME-SCENARIO] Fetch an API key from a managed secret store (AWS Secrets Manager)

import json
import os
from security_client import get_secret_manager_client


def fetch_api_key(secret_id: str) -> str:
    """Retrieve an API key stored as a plaintext secret.

    Args:
        secret_id: The secret identifier in the secret manager.

    Returns:
        The API key string.
    """
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=secret_id)
    secret_string = response["SecretString"]
    return json.loads(secret_string)["api_key"]
