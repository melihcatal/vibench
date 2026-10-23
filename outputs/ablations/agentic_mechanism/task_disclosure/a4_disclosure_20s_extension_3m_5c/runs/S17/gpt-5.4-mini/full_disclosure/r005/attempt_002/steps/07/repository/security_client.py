from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional


DEFAULT_PROVIDER = "google"
DEFAULT_GCP_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "")
DEFAULT_GCP_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
DEFAULT_GCP_KEY_RING = os.getenv("GOOGLE_CLOUD_KMS_KEY_RING", "")
DEFAULT_GCP_CRYPTO_KEY = os.getenv("GOOGLE_CLOUD_KMS_CRYPTO_KEY", "")
DEFAULT_GCP_KEY_VERSION = os.getenv("GOOGLE_CLOUD_KMS_KEY_VERSION", "")


@dataclass(frozen=True)
class SecurityConfig:
    provider: str = DEFAULT_PROVIDER
    project_id: str = DEFAULT_GCP_PROJECT_ID
    location: str = DEFAULT_GCP_LOCATION
    key_ring: str = DEFAULT_GCP_KEY_RING
    crypto_key: str = DEFAULT_GCP_CRYPTO_KEY
    key_version: str = DEFAULT_GCP_KEY_VERSION
    api_endpoint: str = "cloudkms.googleapis.com"

    @property
    def key_name(self) -> str:
        if self.project_id and self.location and self.key_ring and self.crypto_key:
            return (
                f"projects/{self.project_id}/locations/{self.location}"
                f"/keyRings/{self.key_ring}/cryptoKeys/{self.crypto_key}"
            )
        return ""

    @property
    def key_version_name(self) -> str:
        if self.key_name and self.key_version:
            return f"{self.key_name}/cryptoKeyVersions/{self.key_version}"
        return ""


def load_security_config(overrides: Optional[Dict[str, Any]] = None) -> SecurityConfig:
    values: Dict[str, Any] = {
        "provider": os.getenv("SECURITY_PROVIDER", DEFAULT_PROVIDER),
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT", DEFAULT_GCP_PROJECT_ID),
        "location": os.getenv("GOOGLE_CLOUD_LOCATION", DEFAULT_GCP_LOCATION),
        "key_ring": os.getenv("GOOGLE_CLOUD_KMS_KEY_RING", DEFAULT_GCP_KEY_RING),
        "crypto_key": os.getenv("GOOGLE_CLOUD_KMS_CRYPTO_KEY", DEFAULT_GCP_CRYPTO_KEY),
        "key_version": os.getenv("GOOGLE_CLOUD_KMS_KEY_VERSION", DEFAULT_GCP_KEY_VERSION),
        "api_endpoint": os.getenv("GOOGLE_CLOUD_KMS_API_ENDPOINT", "cloudkms.googleapis.com"),
    }
    if overrides:
        values.update({k: v for k, v in overrides.items() if v is not None})
    return SecurityConfig(**values)


@lru_cache(maxsize=1)
def get_default_security_config() -> SecurityConfig:
    return load_security_config()


def build_kms_client_kwargs(config: Optional[SecurityConfig] = None) -> Dict[str, Any]:
    cfg = config or get_default_security_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_endpoint:
        kwargs["client_options"] = {"api_endpoint": cfg.api_endpoint}
    return kwargs


def resolve_encryption_key_name(config: Optional[SecurityConfig] = None) -> str:
    cfg = config or get_default_security_config()
    return cfg.key_name


def resolve_key_version_name(config: Optional[SecurityConfig] = None) -> str:
    cfg = config or get_default_security_config()
    return cfg.key_version_name


def has_complete_kms_config(config: Optional[SecurityConfig] = None) -> bool:
    cfg = config or get_default_security_config()
    return all([cfg.project_id, cfg.location, cfg.key_ring, cfg.crypto_key])


def get_kms_provider_name(config: Optional[SecurityConfig] = None) -> str:
    cfg = config or get_default_security_config()
    return cfg.provider
