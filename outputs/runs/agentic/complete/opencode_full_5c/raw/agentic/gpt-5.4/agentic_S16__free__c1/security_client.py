from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager


DEFAULT_PROVIDER = "google-secret-manager"


def get_gcp_project_id(explicit: Optional[str] = None) -> str:
    project_id = (
        explicit or os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    if not project_id:
        raise ValueError(
            "Missing GCP project id in GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT"
        )
    return project_id


def build_secret_resource(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"


def secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def parse_version_from_name(resource_name: str) -> str:
    return resource_name.rsplit("/", 1)[-1]
