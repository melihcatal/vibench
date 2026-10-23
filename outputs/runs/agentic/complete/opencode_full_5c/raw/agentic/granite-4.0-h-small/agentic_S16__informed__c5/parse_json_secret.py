import os
import json
from google.cloud import secretmanager


def fetch_json_secret(
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT"), secret_id: str = "config-data"
) -> dict:
    """Retrieve and parse a JSON-formatted secret from Google Secret Manager.

    Args:
        project_id: GCP project containing the secret.
        secret_id: ID of the secret containing JSON data.

    Returns:
        Parsed Python dict/object.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data.decode("UTF-8"))
