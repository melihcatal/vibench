import base64
import os
from typing import Optional

from google.cloud import kms_v1

from security_models import SecurityConfig


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        google_project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        google_location=os.getenv("GOOGLE_CLOUD_LOCATION", "global"),
        google_key_ring=os.getenv("GOOGLE_KMS_KEY_RING"),
        google_key_name=os.getenv("GOOGLE_KMS_KEY_NAME"),
        google_key_version=os.getenv("GOOGLE_KMS_KEY_VERSION"),
        google_kms_key_path=os.getenv("GOOGLE_KMS_KEY_PATH"),
    )


def kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def build_kms_key_path(config: SecurityConfig, key_name: Optional[str] = None) -> str:
    if config.google_kms_key_path:
        return config.google_kms_key_path
    if not config.google_project_id or not config.google_key_ring:
        raise ValueError("Google Cloud project and key ring are required")
    name = key_name or config.google_key_name
    if not name:
        raise ValueError("Google KMS key name is required")
    return kms_client().crypto_key_path(config.google_project_id, config.google_location, config.google_key_ring, name)


def encode_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def decode_bytes(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))
