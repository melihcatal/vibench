from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager

from security_client import get_project_id, get_secret_client, resolve_version_name
from security_models import DBSecret, SecretValueResult


_PROVIDER = "google-cloud-secret-manager"


def fetch_db_secret(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> DBSecret:
    client = get_secret_client()
    project = project_id or get_project_id()
    name = resolve_version_name(project, secret_id, version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    result = SecretValueResult(provider=_PROVIDER, secret_id=secret_id, version=version, value=payload)
    return DBSecret.from_secret_value(result)


if __name__ == "__main__":
    secret_id = os.environ.get("SECRET_ID", "db-connection")
    secret = fetch_db_secret(secret_id=secret_id, version=os.environ.get("SECRET_VERSION", "latest"))
    print(secret.connection_string)
