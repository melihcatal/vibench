from google.cloud import secretmanager
import os
from security_client import get_google_project
from security_models import parse_json_secret
from typing import Dict, Any

def retrieve_and_parse_json_secret(secret_name: str) -> Dict[str, Any]:
    project = get_google_project()
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    secret_value = response.payload.data.decode('UTF-8')
    return parse_json_secret(secret_value)
