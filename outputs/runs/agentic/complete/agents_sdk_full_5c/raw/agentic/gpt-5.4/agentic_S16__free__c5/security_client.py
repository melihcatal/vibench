from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager

from security_models import SecretReference


DEFAULT_GCP_PROJECT_ENV = "GCP_PROJECT_ID"
DEFAULT_GOOGLE_REGION_ENV = "GOOGLE_CLOUD_REGION"


class SecretManagerConfig:
    def __init__(self, project_id: Optional[str] = None, region: Optional[str] = None) -> None:
        self.project_id = project_id or os.getenv(DEFAULT_GCP_PROJECT_ENV) or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.region = region or os.getenv(DEFAULT_GOOGLE_REGION_ENV, "global")
        if not self.project_id:
            raise ValueError("Missing GCP project id. Set GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT.")



def load_config(project_id: Optional[str] = None) -> SecretManagerConfig:
    return SecretManagerConfig(project_id=project_id)



def build_secret_reference(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> SecretReference:
    config = load_config(project_id=project_id)
    return SecretReference(project_id=config.project_id, secret_id=secret_id, version=version)



def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()
