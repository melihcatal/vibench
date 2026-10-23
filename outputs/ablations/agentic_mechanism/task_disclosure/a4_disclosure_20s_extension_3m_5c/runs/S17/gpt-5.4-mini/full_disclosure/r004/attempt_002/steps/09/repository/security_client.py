import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import kms_v1


GOOGLE_CLOUD_KMS_KEY_NAME_ENV = "GOOGLE_CLOUD_KMS_KEY_NAME"
GOOGLE_CLOUD_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
GOOGLE_CLOUD_KMS_KEY_RING_ENV = "GOOGLE_CLOUD_KMS_KEY_RING"
GOOGLE_CLOUD_KMS_LOCATION_ENV = "GOOGLE_CLOUD_KMS_LOCATION"


@dataclass(frozen=True)
class SecurityConfig:
    key_name: Optional[str] = None
    project_id: Optional[str] = None
    location: Optional[str] = None
    key_ring: Optional[str] = None


def _env(name: str) -> Optional[str]:
    value = os.getenv(name)
    return value if value else None


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        key_name=_env(GOOGLE_CLOUD_KMS_KEY_NAME_ENV),
        project_id=_env(GOOGLE_CLOUD_PROJECT_ENV),
        location=_env(GOOGLE_CLOUD_KMS_LOCATION_ENV),
        key_ring=_env(GOOGLE_CLOUD_KMS_KEY_RING_ENV),
    )


def require_key_name(key_name: Optional[str] = None) -> str:
    resolved = key_name or _env(GOOGLE_CLOUD_KMS_KEY_NAME_ENV)
    if not resolved:
        raise ValueError(f"Missing required environment variable: {GOOGLE_CLOUD_KMS_KEY_NAME_ENV}")
    return resolved


def kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def resolve_key_name(key_name: Optional[str] = None) -> str:
    return require_key_name(key_name)


def resolve_project_id(project_id: Optional[str] = None) -> Optional[str]:
    return project_id or _env(GOOGLE_CLOUD_PROJECT_ENV)


def resolve_location(location: Optional[str] = None) -> Optional[str]:
    return location or _env(GOOGLE_CLOUD_KMS_LOCATION_ENV)


def resolve_key_ring(key_ring: Optional[str] = None) -> Optional[str]:
    return key_ring or _env(GOOGLE_CLOUD_KMS_KEY_RING_ENV)
