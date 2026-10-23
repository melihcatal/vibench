from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from google.cloud import secretmanager


def get_gcp_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or "demo-project"


@lru_cache(maxsize=1)
def secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def get_secret_version_name(project_id: str, secret_id: str, version: str = "latest") -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def get_region() -> Optional[str]:
    return os.environ.get("GOOGLE_CLOUD_REGION")
