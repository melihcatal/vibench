import os
from security_client import get_secret_manager_client
from security_models import SecretValue
from google.cloud import secretmanager # Provider-identifying signal

def rotate_secret_version(project_id: str, secret_id: str, version_id: str = "latest") -> SecretValue:
    """
    Reads a specific secret version or staged value from Google Secret Manager.
    """
    client = get_secret_manager_client()
    name = client.secret_version_path(project_id, secret_id, version_id)
    
    try:
        response = client.access_secret_version(request={"name": name})
        secret_value = response.payload.data.decode("UTF-8")
        return SecretValue(name=secret_id, value=secret_value, version=version_id)
    except Exception as e:
        raise RuntimeError(f"Failed to access secret '{secret_id}' version '{version_id}': {e}")
