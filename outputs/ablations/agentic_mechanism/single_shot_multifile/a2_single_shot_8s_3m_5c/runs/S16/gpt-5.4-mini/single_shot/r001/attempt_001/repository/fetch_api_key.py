import os
from typing import Any, Dict, Optional
from google.cloud import secretmanager
from security_client import get_secret_manager_client, resolve_secret_name, secret_version_path
from security_models import SecretValue


def fetch_api_key(secret_name: Optional[str] = None, version: str = "latest") -> SecretValue:
    client = get_secret_manager_client()
    resource = resolve_secret_name(secret_name or os.environ.get("GCP_API_KEY_SECRET", "api-key"))
    name = secret_version_path(resource, version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    return SecretValue(name=resource, version=version, value=payload)
