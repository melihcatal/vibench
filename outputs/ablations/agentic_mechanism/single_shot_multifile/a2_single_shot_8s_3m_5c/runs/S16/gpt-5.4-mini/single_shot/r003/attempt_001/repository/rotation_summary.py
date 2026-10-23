from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager

from security_client import get_project_id, get_secret_client, resolve_version_name
from security_models import RotationSummary


_PROVIDER = "google-cloud-secret-manager"


def rotation_summary(secret_id: str, current_version: str, project_id: Optional[str] = None) -> RotationSummary:
    client = get_secret_client()
    project = project_id or get_project_id()
    name = resolve_version_name(project, secret_id, current_version)
    client.access_secret_version(request={"name": name})
    return RotationSummary(provider=_PROVIDER, secret_id=secret_id, current_version=current_version, status="active")


if __name__ == "__main__":
    secret_id = os.environ.get("SECRET_ID", "rotating-secret")
    current_version = os.environ.get("SECRET_VERSION", "latest")
    summary = rotation_summary(secret_id, current_version)
    print(summary.status)
