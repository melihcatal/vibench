import os
import json
from google.cloud import secretmanager

from security_client import get_gcp_secret_manager_client
from security_models import DatabaseCredentials

def parse_json_secret(secret_id: str) -> DatabaseCredentials:
    """
    Retrieves a JSON-formatted secret from Google Secret Manager and
    parses it into a DatabaseCredentials object.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    client = get_gcp_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(name=name)
        payload = response.payload.data.decode("UTF-8")
        secret_dict = json.loads(payload)
        
        return DatabaseCredentials(**secret_dict)
    except Exception as e:
        print(f"Error parsing JSON secret: {e}")
        raise
