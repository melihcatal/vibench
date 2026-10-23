from __future__ import annotations

import os
from typing import Any

from google.cloud import secretmanager

from security_models import decode_secret_bytes, normalize_secret_resource


def get_gcp_project_id() -> str:
    project_id = os.environ.get("GCP_PROJECT_ID") or os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )
    if not project_id:
        raise ValueError("Missing GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT")
    return project_id


def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def access_secret_value(
    secret_id: str, version_id: str = "latest", project_id: str | None = None
) -> dict[str, Any]:
    resolved_project = project_id or get_gcp_project_id()
    name = normalize_secret_resource(resolved_project, secret_id, version_id)
    client = get_secret_manager_client()
    response = client.access_secret_version(request={"name": name})
    return {
        "name": name,
        "project_id": resolved_project,
        "secret_id": secret_id,
        "version_id": version_id,
        "value": decode_secret_bytes(response.payload.data),
        "response": response,
    }


def get_secret_metadata(secret_id: str, project_id: str | None = None) -> Any:
    resolved_project = project_id or get_gcp_project_id()
    client = get_secret_manager_client()
    name = f"projects/{resolved_project}/secrets/{secret_id}"
    return client.get_secret(request={"name": name})


def get_secret_version_metadata(
    secret_id: str, version_id: str, project_id: str | None = None
) -> Any:
    resolved_project = project_id or get_gcp_project_id()
    client = get_secret_manager_client()
    name = normalize_secret_resource(resolved_project, secret_id, version_id)
    return client.get_secret_version(request={"name": name})
