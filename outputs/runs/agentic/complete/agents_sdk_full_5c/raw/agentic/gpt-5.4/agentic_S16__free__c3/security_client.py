from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager

from security_models import SecretReference


DEFAULT_GCP_PROJECT_ENV = "GCP_PROJECT_ID"
DEFAULT_SECRET_VERSION = "latest"


def get_project_id(explicit_project_id: Optional[str] = None) -> str:
    project_id = explicit_project_id or os.getenv(DEFAULT_GCP_PROJECT_ENV) or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Missing GCP project id. Set GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT.")
    return project_id


def build_secret_version_name(secret_id: str, project_id: Optional[str] = None, version_id: str = DEFAULT_SECRET_VERSION) -> str:
    resolved_project = get_project_id(project_id)
    return f"projects/{resolved_project}/secrets/{secret_id}/versions/{version_id}"


def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def as_reference(secret_id: str, project_id: Optional[str] = None, version_id: str = DEFAULT_SECRET_VERSION) -> SecretReference:
    return SecretReference(secret_id=secret_id, project_id=get_project_id(project_id), version_id=version_id)
