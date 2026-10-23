from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from google.cloud import kms_v1


@dataclass(frozen=True)
class SecurityClientConfig:
    project_id: Optional[str] = None
    location_id: str = "global"
    key_ring_id: Optional[str] = None
    key_id: Optional[str] = None
    key_version_id: Optional[str] = None
    credentials_path: Optional[str] = None

    @classmethod
    def from_env(cls) -> "SecurityClientConfig":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
            location_id=os.getenv("GOOGLE_CLOUD_KMS_LOCATION", "global"),
            key_ring_id=os.getenv("GOOGLE_CLOUD_KMS_KEY_RING"),
            key_id=os.getenv("GOOGLE_CLOUD_KMS_KEY"),
            key_version_id=os.getenv("GOOGLE_CLOUD_KMS_KEY_VERSION"),
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        )


def normalize_resource_name(resource: str) -> str:
    return resource.strip().replace("//", "/")


def build_crypto_key_path(config: SecurityClientConfig) -> Optional[str]:
    if not (config.project_id and config.location_id and config.key_ring_id and config.key_id):
        return None
    client = kms_v1.KeyManagementServiceClient()
    return client.crypto_key_path(config.project_id, config.location_id, config.key_ring_id, config.key_id)


def build_crypto_key_version_path(config: SecurityClientConfig) -> Optional[str]:
    if not (config.project_id and config.location_id and config.key_ring_id and config.key_id and config.key_version_id):
        return None
    client = kms_v1.KeyManagementServiceClient()
    return client.crypto_key_version_path(
        config.project_id,
        config.location_id,
        config.key_ring_id,
        config.key_id,
        config.key_version_id,
    )


@lru_cache(maxsize=1)
def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def get_config_overrides(**overrides: Any) -> SecurityClientConfig:
    base = SecurityClientConfig.from_env()
    return SecurityClientConfig(
        project_id=overrides.get("project_id", base.project_id),
        location_id=overrides.get("location_id", base.location_id),
        key_ring_id=overrides.get("key_ring_id", base.key_ring_id),
        key_id=overrides.get("key_id", base.key_id),
        key_version_id=overrides.get("key_version_id", base.key_version_id),
        credentials_path=overrides.get("credentials_path", base.credentials_path),
    )


def client_metadata(config: Optional[SecurityClientConfig] = None) -> Dict[str, Any]:
    cfg = config or SecurityClientConfig.from_env()
    return {
        "provider": "google-cloud-kms",
        "project_id": cfg.project_id,
        "location_id": cfg.location_id,
        "key_ring_id": cfg.key_ring_id,
        "key_id": cfg.key_id,
        "key_version_id": cfg.key_version_id,
    }
