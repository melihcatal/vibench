from google.cloud import secretmanager
from google.cloud.secretmanager import SecretVersionName
import json
from typing import Dict, Any
from security_client import get_gcp_project


def fetch_db_secret(secret_id: str) -> Dict[str, Any]:
    project = get_gcp_project()
    client = secretmanager.SecretManagerServiceClient()
    name = SecretVersionName(project, secret_id, "latest").name
    response = client.access_secret_version(request={"name": name})
    secret_value = response.payload.data.decode("UTF-8")
    return json.loads(secret_value)
