import os
from typing import Optional
from google.cloud import secretmanager
from security_client import get_secret_manager_client, resolve_secret_name, secret_version_path
from security_models import SecretVersionRead


def rotate_secret_version(secret_name: Optional[str] = None, version: str = "latest") -> SecretVersionRead:
    client = get_secret_manager_client()
    resource = resolve_secret_name(secret_name or os.environ.get("GCP_ROTATE_SECRET", "rotating-secret"))
    name = secret_version_path(resource, version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    return SecretVersionRead(name=resource, version=version, value=payload)
