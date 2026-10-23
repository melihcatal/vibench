import os
import json
from security_client import get_google_secret_manager_client
from security_models import SecretItem

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> dict:
    client = get_google_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    try:
        response = client.access_secret_version(request={"name": name})
        secret_payload = response.payload.data.decode("UTF-8")
        return json.loads(secret_payload)
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve and parse JSON secret from Google Secret Manager: {e}")
