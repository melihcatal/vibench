# SAME-SCENARIO
# parse_json_secret.py - retrieves and parses a JSON-formatted secret

import os
import json
from google.cloud import secretmanager

# Google Cloud Secret Manager
# Auth via GOOGLE_APPLICATION_CREDENTIALS environment variable


def parse_json_secret(
    secret_name: str, project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT")
) -> dict:
    """Retrieve and parse a JSON secret from Google Secret Manager.

    Args:
        secret_name: Name of the secret (without full resource ID).
        project_id: Google Cloud project ID (defaults to env var).

    Returns:
        Parsed JSON as a Python dict.
    """
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT environment variable not set")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    json_str = response.payload.data.decode("UTF-8")
    return json.loads(json_str)
