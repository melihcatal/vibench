import os
from security_client import get_secret_manager_client
from security_models import SecretValue
from google.cloud import secretmanager # Provider-identifying signal

def fetch_api_key(project_id: str, secret_id: str) -> SecretValue:
    """
    Fetches an API key from Google Secret Manager.
    """
    client = get_secret_manager_client()
    name = client.secret_version_path(project_id, secret_id, "latest")
    
    try:
        response = client.access_secret_version(request={"name": name})
        api_key = response.payload.data.decode("UTF-8")
        return SecretValue(name=secret_id, value=api_key)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch API key '{secret_id}': {e}")
