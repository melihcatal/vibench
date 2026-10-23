import os
from typing import Optional
from google.cloud import secretmanager
from security_client import get_secret_manager_client, resolve_secret_name, secret_version_path
from security_models import DatabaseSecret, parse_database_secret


def fetch_db_secret(secret_name: Optional[str] = None, version: str = "latest") -> DatabaseSecret:
    client = get_secret_manager_client()
    resource = resolve_secret_name(secret_name or os.environ.get("GCP_DB_SECRET", "db-connection"))
    name = secret_version_path(resource, version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    return parse_database_secret(payload, secret_name=resource, version=version)
