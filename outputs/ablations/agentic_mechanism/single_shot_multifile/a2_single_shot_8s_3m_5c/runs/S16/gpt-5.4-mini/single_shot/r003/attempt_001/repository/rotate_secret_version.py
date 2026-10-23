from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager

from security_client import get_project_id, get_secret_client, resolve_version_name
from security_models import SecretValueResult


_PROVIDER = "google-cloud-secret-manager"


def rotate_secret_version(secret_id: str, version: str, project_id: Optional[str] = None) -> SecretValueResult:
    client = get_secret_client()
    project = project_id or get_project_id()
    name = resolve_version_name(project, secret_id, version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    return SecretValueResult(provider=_PROVIDER, secret_id=secret_id, version=version, value=payload, stage=getattr(response, "name", name))


if __name__ == "__main__":
    secret_id = os.environ.get("SECRET_ID", "rotating-secret")
    version = os.environ.get("SECRET_VERSION", "latest")
    result = rotate_secret_version(secret_id=secret_id, version=version)
    print(result.value)
