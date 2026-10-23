from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import kms_v1


@dataclass(frozen=True)
class SecurityConfig:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str


def load_security_config() -> SecurityConfig:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    location_id = os.getenv("GOOGLE_CLOUD_KMS_LOCATION", "global")
    key_ring_id = os.getenv("GOOGLE_CLOUD_KMS_KEY_RING", "default-key-ring")
    crypto_key_id = os.getenv("GOOGLE_CLOUD_KMS_CRYPTO_KEY_ID", "default-crypto-key")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT must be set")
    return SecurityConfig(project_id=project_id, location_id=location_id, key_ring_id=key_ring_id, crypto_key_id=crypto_key_id)


def build_kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def resolve_crypto_key_name(key_name: Optional[str] = None) -> str:
    if key_name:
        return key_name
    config = load_security_config()
    return f"projects/{config.project_id}/locations/{config.location_id}/keyRings/{config.key_ring_id}/cryptoKeys/{config.crypto_key_id}"
