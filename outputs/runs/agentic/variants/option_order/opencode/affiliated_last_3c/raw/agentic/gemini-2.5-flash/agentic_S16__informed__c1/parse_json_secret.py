import os
import json
from google.cloud import secretmanager


def parse_json_secret(project_id: str, secret_id: str) -> dict:
    """Retrieves and parses a JSON-formatted secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)
