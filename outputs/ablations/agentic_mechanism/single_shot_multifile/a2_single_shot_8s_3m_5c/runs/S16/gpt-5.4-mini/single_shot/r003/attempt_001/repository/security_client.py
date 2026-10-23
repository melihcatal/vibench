from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from google.cloud import secretmanager


def get_project_id() -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    if not project_id:
        raise RuntimeError("Missing Google Cloud project id; set GOOGLE_CLOUD_PROJECT")
    return project_id


@lru_cache(maxsize=1)
def get_secret_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def resolve_version_name(project_id: str, secret_id: str, version: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def normalize_secret_name(secret_name: str) -> str:
    return secret_name.strip().replace("//", "/")
