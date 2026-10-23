import os
from security_client import get_secret_manager_client
from security_models import JsonSecret
from google.cloud import secretmanager # Provider-identifying signal

def parse_json_secret(project_id: str, secret_id: str) -> JsonSecret:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    """
    client = get_secret_manager_client()
    name = client.secret_version_path(project_id, secret_id, "latest")
    
    try:
        response = client.access_secret_version(request={"name": name})
        json_string = response.payload.data.decode("UTF-8")
        return JsonSecret.from_string(name=secret_id, json_string=json_string)
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve and parse JSON secret '{secret_id}': {e}")
