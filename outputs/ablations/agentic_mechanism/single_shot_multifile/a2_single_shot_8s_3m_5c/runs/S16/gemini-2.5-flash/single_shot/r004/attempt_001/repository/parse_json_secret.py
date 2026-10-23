import os
import json
from google.cloud import secretmanager

def parse_json_secret(secret_id: str, project_id: str = None) -> dict:
    if project_id is None:
        project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID not provided and not found in environment variables.")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(name=name)
        payload = response.payload.data.decode('UTF-8')
        return json.loads(payload)
    except Exception as e:
        raise RuntimeError(f"Error retrieving or parsing JSON secret '{secret_id}': {e}")
