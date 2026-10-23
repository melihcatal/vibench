import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import kms_v1


DEFAULT_PROVIDER = "google_cloud_kms"


@dataclass(frozen=True)
class SecurityConfig:
    provider: str = DEFAULT_PROVIDER
    gcp_kms_key_name: Optional[str] = None
    gcp_project_id: Optional[str] = None
    gcp_location_id: Optional[str] = None
    gcp_key_ring_id: Optional[str] = None
    gcp_crypto_key_id: Optional[str] = None


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        provider=os.getenv("SECURITY_PROVIDER", DEFAULT_PROVIDER),
        gcp_kms_key_name=os.getenv("GCP_KMS_KEY_NAME"),
        gcp_project_id=os.getenv("GCP_PROJECT_ID"),
        gcp_location_id=os.getenv("GCP_KMS_LOCATION_ID"),
        gcp_key_ring_id=os.getenv("GCP_KMS_KEY_RING_ID"),
        gcp_crypto_key_id=os.getenv("GCP_KMS_CRYPTO_KEY_ID"),
    )


@lru_cache(maxsize=1)
def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def get_default_key_name() -> str:
    config = load_security_config()
    if config.gcp_kms_key_name:
        return config.gcp_kms_key_name
    if all([config.gcp_project_id, config.gcp_location_id, config.gcp_key_ring_id, config.gcp_crypto_key_id]):
        return (
            f"projects/{config.gcp_project_id}/locations/{config.gcp_location_id}/"
            f"keyRings/{config.gcp_key_ring_id}/cryptoKeys/{config.gcp_crypto_key_id}"
        )
    raise ValueError("GCP_KMS_KEY_NAME or the GCP key path components must be set")


def get_provider() -> str:
    return load_security_config().provider


def ensure_google_cloud_kms() -> kms_v1.KeyManagementServiceClient:
    if get_provider() != DEFAULT_PROVIDER:
        raise ValueError(f"Unsupported provider: {get_provider()}")
    return get_kms_client()
