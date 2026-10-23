from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import kms
from google.cloud.kms_v1.services.key_management_service import KeyManagementServiceClient
from google.oauth2 import service_account


@dataclass(frozen=True)
class SecurityConfig:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    key_version_id: str = "1"
    api_key: Optional[str] = None
    gcp_credentials_b64: Optional[str] = None

    @property
    def crypto_key_path(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location_id}/keyRings/{self.key_ring_id}/cryptoKeys/{self.crypto_key_id}"

    @property
    def crypto_key_version_path(self) -> str:
        return f"{self.crypto_key_path}/cryptoKeyVersions/{self.key_version_id}"


@lru_cache(maxsize=1)
def load_config() -> SecurityConfig:
    return SecurityConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", "demo-project"),
        location_id=os.environ.get("GCP_KMS_LOCATION", "us-central1"),
        key_ring_id=os.environ.get("GCP_KMS_KEY_RING", "security-ring"),
        crypto_key_id=os.environ.get("GCP_KMS_CRYPTO_KEY", "security-key"),
        key_version_id=os.environ.get("GCP_KMS_KEY_VERSION", "1"),
        api_key=os.environ.get("GOOGLE_API_KEY"),
        gcp_credentials_b64=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_B64"),
    )


@lru_cache(maxsize=1)
def get_kms_client() -> KeyManagementServiceClient:
    cfg = load_config()
    if cfg.gcp_credentials_b64:
        data = base64.b64decode(cfg.gcp_credentials_b64)
        creds = service_account.Credentials.from_service_account_info(__import__("json").loads(data.decode("utf-8")))
        return kms.KeyManagementServiceClient(credentials=creds)
    return kms.KeyManagementServiceClient()


def normalize_key_path(resource_name: Optional[str] = None) -> str:
    return resource_name or load_config().crypto_key_path


def normalize_key_version_path(resource_name: Optional[str] = None) -> str:
    return resource_name or load_config().crypto_key_version_path
