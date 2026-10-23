import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SecurityConfig:
    google_kms_key_name: str
    google_project_id: str
    google_location: str
    google_key_ring: str
    google_key_name: str
    google_kms_endpoint: str
    google_credentials_path: Optional[str]


def load_security_config() -> SecurityConfig:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    key_ring = os.getenv("GOOGLE_KMS_KEY_RING", "default-ring")
    key_name = os.getenv("GOOGLE_KMS_KEY_NAME", "default-key")
    kms_endpoint = os.getenv("GOOGLE_KMS_API_ENDPOINT", "cloudkms.googleapis.com")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    key_resource = os.getenv(
        "GOOGLE_KMS_KEY_NAME_FULL",
        f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key_name}",
    )
    return SecurityConfig(
        google_kms_key_name=key_resource,
        google_project_id=project_id,
        google_location=location,
        google_key_ring=key_ring,
        google_key_name=key_name,
        google_kms_endpoint=kms_endpoint,
        google_credentials_path=credentials_path,
    )


def google_kms_client_kwargs() -> dict:
    config = load_security_config()
    kwargs = {"client_options": {"api_endpoint": config.google_kms_endpoint}}
    if config.google_credentials_path:
        kwargs["credentials"] = config.google_credentials_path
    return kwargs
