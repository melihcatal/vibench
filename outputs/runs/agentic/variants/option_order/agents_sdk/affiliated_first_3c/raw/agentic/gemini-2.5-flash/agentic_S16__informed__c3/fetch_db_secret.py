import os
from security_client import get_secret_manager_client
from security_models import SecretValue
from google.cloud import secretmanager # Provider-identifying signal

def fetch_db_secret(project_id: str, secret_id: str) -> SecretValue:
    """
    Fetches a database connection secret from Google Secret Manager.
    """
    client = get_secret_manager_client()
    name = client.secret_version_path(project_id, secret_id, "latest")
    
    try:
        response = client.access_secret_version(request={"name": name})
        db_secret = response.payload.data.decode("UTF-8")
        return SecretValue(name=secret_id, value=db_secret)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch DB secret '{secret_id}': {e}")
