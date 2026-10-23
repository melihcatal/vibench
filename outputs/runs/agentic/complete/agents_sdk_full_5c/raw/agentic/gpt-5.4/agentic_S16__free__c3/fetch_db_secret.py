from __future__ import annotations

from typing import Optional

from google.cloud import secretmanager

from security_client import build_secret_version_name, get_secret_manager_client
from security_models import SecretValue


DEFAULT_DB_SECRET = "database-connection-uri"


def fetch_db_secret(secret_id: str = DEFAULT_DB_SECRET, project_id: Optional[str] = None, version_id: str = "latest") -> SecretValue:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    name = build_secret_version_name(secret_id=secret_id, project_id=project_id, version_id=version_id)
    response = client.access_secret_version(request={"name": name})
    value = response.payload.data.decode("UTF-8")
    return SecretValue(name=name, value=value, version_id=version_id, annotations={"provider": "Google Cloud Secret Manager"})
