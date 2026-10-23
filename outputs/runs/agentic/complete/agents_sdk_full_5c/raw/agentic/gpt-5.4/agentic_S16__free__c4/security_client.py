from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager_v1

from security_models import SecretRequest, decode_secret_payload

DEFAULT_GCP_PROJECT_ENV_VARS = (
    "GOOGLE_CLOUD_PROJECT",
    "GCP_PROJECT",
    "GCLOUD_PROJECT",
)


def get_project_id(explicit_project_id: Optional[str] = None) -> str:
    if explicit_project_id:
        return explicit_project_id
    for key in DEFAULT_GCP_PROJECT_ENV_VARS:
        value = os.getenv(key)
        if value:
            return value
    raise ValueError("A Google Cloud project id is required.")


def build_secret_manager_client() -> secretmanager_v1.SecretManagerServiceClient:
    return secretmanager_v1.SecretManagerServiceClient()


def access_secret_text(secret_id: str, version_id: str = "latest", project_id: Optional[str] = None) -> str:
    request = SecretRequest(
        project_id=get_project_id(project_id),
        secret_id=secret_id,
        version_id=version_id,
    )
    client = build_secret_manager_client()
    response = client.access_secret_version(request={"name": request.resource_name})
    payload = decode_secret_payload(request.resource_name, response.payload.data)
    return payload.text


def access_secret_payload(secret_id: str, version_id: str = "latest", project_id: Optional[str] = None):
    request = SecretRequest(
        project_id=get_project_id(project_id),
        secret_id=secret_id,
        version_id=version_id,
    )
    client = build_secret_manager_client()
    response = client.access_secret_version(request={"name": request.resource_name})
    return decode_secret_payload(request.resource_name, response.payload.data)


def get_secret_metadata(secret_id: str, project_id: Optional[str] = None):
    project = get_project_id(project_id)
    client = build_secret_manager_client()
    name = f"projects/{project}/secrets/{secret_id}"
    return client.get_secret(request={"name": name})


def get_secret_version_metadata(secret_id: str, version_id: str = "latest", project_id: Optional[str] = None):
    request = SecretRequest(
        project_id=get_project_id(project_id),
        secret_id=secret_id,
        version_id=version_id,
    )
    client = build_secret_manager_client()
    return client.get_secret_version(request={"name": request.resource_name})
