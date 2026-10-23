from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager_v1


GCP_PROJECT_ID_ENV = "GCP_PROJECT_ID"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TRANSLATION_MODEL = "gpt-4o-mini"


def get_project_id(explicit_project_id: Optional[str] = None) -> str:
    project_id = (
        explicit_project_id
        or os.getenv(GCP_PROJECT_ID_ENV)
        or os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    if not project_id:
        raise ValueError(
            "A Google Cloud project ID is required via GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT"
        )
    return project_id


def build_secret_manager_client() -> secretmanager_v1.SecretManagerServiceClient:
    return secretmanager_v1.SecretManagerServiceClient()


def build_secret_version_name(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"


def build_secret_name(project_id: str, secret_id: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}"
