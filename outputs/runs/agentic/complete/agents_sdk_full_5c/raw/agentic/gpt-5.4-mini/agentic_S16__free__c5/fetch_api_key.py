import os
from typing import Optional

from security_client import get_secret_manager_client, get_secret_name
from security_models import SecretFetchRequest, normalize_secret_payload, build_string_payload

# Google Cloud Secret Manager integration
from google.cloud import secretmanager


def fetch_api_key(version: str = "latest", project_id: Optional[str] = None, secret_id: Optional[str] = None) -> str:
    project = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    name = get_secret_name(project, secret_id or os.getenv("API_KEY_SECRET_ID", "api-key"))
    client = get_secret_manager_client()
    request = SecretFetchRequest(secret_name=name, version=version)
    response = client.access_secret_version(name=request.versioned_name())
    payload = normalize_secret_payload(response.payload.data)
    return build_string_payload(payload)
