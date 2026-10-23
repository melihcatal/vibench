from google.cloud import secretmanager
from typing import Dict, Any
import os

from security_client import get_secrets_config

def fetch_db_secret(secret_id: str) -> str:
    config = get_secrets_config()
    project = config['gcp_project_id']
    full_name = f"projects/{project}/secrets/{secret_id}/versions/latest"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=full_name)
    return response.payload.data.decode("UTF-8")