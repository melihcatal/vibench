from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager

from security_models import SecretReference


DEFAULT_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
GOOGLE_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


def get_project_id(explicit_project_id: Optional[str] = None) -> str:
    project_id = explicit_project_id or os.getenv(DEFAULT_PROJECT_ENV)
    if not project_id:
        raise ValueError(
            f"Missing Google Cloud project id. Set {DEFAULT_PROJECT_ENV} or pass project_id explicitly."
        )
    return project_id


def build_secret_reference(secret_id: str, version_id: str = "latest", project_id: Optional[str] = None) -> SecretReference:
    return SecretReference(
        project_id=get_project_id(project_id),
        secret_id=secret_id,
        version_id=version_id,
    )


def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def access_secret_version(secret_id: str, version_id: str = "latest", project_id: Optional[str] = None):
    client = get_secret_manager_client()
    ref = build_secret_reference(secret_id=secret_id, version_id=version_id, project_id=project_id)
    return client.access_secret_version(request={"name": ref.resource_name})


def get_secret_value(secret_id: str, version_id: str = "latest", project_id: Optional[str] = None) -> str:
    response = access_secret_version(secret_id=secret_id, version_id=version_id, project_id=project_id)
    return response.payload.data.decode("utf-8")


def get_secret_metadata(secret_id: str, project_id: Optional[str] = None):
    client = get_secret_manager_client()
    project = get_project_id(project_id)
    name = f"projects/{project}/secrets/{secret_id}"
    return client.get_secret(request={"name": name})


def list_secret_versions(secret_id: str, project_id: Optional[str] = None):
    client = get_secret_manager_client()
    project = get_project_id(project_id)
    parent = f"projects/{project}/secrets/{secret_id}"
    return list(client.list_secret_versions(request={"parent": parent}))
