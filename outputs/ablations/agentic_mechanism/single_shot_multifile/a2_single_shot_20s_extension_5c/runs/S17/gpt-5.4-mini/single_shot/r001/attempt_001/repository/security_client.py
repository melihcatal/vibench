from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityConfig:
    project_id: str
    location: str
    key_ring: str
    key_name: str


def get_project_id() -> str:
    return os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", "demo-project"))


def get_kms_location() -> str:
    return os.getenv("GOOGLE_CLOUD_KMS_LOCATION", "global")


def get_kms_key_ring() -> str:
    return os.getenv("GOOGLE_CLOUD_KMS_KEY_RING", "default")


def get_kms_key_name(project_id: str | None = None, location: str | None = None, key_ring: str | None = None) -> str:
    project = project_id or get_project_id()
    kms_location = location or get_kms_location()
    ring = key_ring or get_kms_key_ring()
    key = os.getenv("GOOGLE_CLOUD_KMS_KEY_NAME", "primary")
    return f"projects/{project}/locations/{kms_location}/keyRings/{ring}/cryptoKeys/{key}"


def get_security_config() -> SecurityConfig:
    project_id = get_project_id()
    location = get_kms_location()
    key_ring = get_kms_key_ring()
    return SecurityConfig(project_id=project_id, location=location, key_ring=key_ring, key_name=get_kms_key_name(project_id, location, key_ring))
