# [SAME-SCENARIO] parse_json_secret.py
# Retrieve and parse a JSON-formatted secret from Google Secrets Manager

import os
from google.cloud import secretmanager

# Google secret manager client uses credentials from env var GOOGLE_APPLICATION_CREDENTIALS
client = secretmanager.SecretManagerServiceClient()


def parse_json_secret(name: str) -> dict:
    """Retrieve a JSON secret and parse it into a Python dictionary.

    Args:
        name: Full resource name of the secret (e.g., projects/123/secrets/api-key/versions/latest)

    Returns:
        Dictionary representation of the JSON secret.
    """
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode("UTF-8")
    return json.loads(payload)
