# parse_json_secret.py
# [SAME-SCENARIO]
# Retrieves and parses a JSON-formatted secret from Google Secret Manager

import os
import json
from google.cloud import secretmanager
from google.auth.exceptions import DefaultCredentialsError


def parse_json_secret(secret_name: str) -> dict:
    """Load a secret that contains JSON and return it as a Python dict.

    Args:
        secret_name: Full resource name of the secret, e.g. projects/*/secrets/*

    Returns:
        Parsed JSON data.
    """
    credentials_env = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_env:
        raise RuntimeError(
            "Set GOOGLE_APPLICATION_CREDENTIALS to point at service account JSON"
        )

    client = secretmanager.SecretManagerServiceClient(credentials=credentials_env)

    try:
        response = client.access_secret_version(name=secret_name)
        secret_payload = response.payload.data.decode("UTF-8")
        return json.loads(secret_payload)
    except DefaultCredentialsError:
        raise RuntimeError("Failed to load Google credentials")
