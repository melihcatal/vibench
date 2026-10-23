import os
from typing import Dict

from google.cloud import kms_v1

from security_models import normalize_text


def load_google_kms_config() -> Dict[str, str]:
    return {
        "project_id": normalize_text(os.getenv("GOOGLE_CLOUD_PROJECT")),
        "location": normalize_text(os.getenv("GOOGLE_CLOUD_KMS_LOCATION", "global")),
        "key_ring": normalize_text(os.getenv("GOOGLE_CLOUD_KMS_KEY_RING")),
        "crypto_key": normalize_text(os.getenv("GOOGLE_CLOUD_KMS_CRYPTO_KEY")),
    }


def kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def key_version_path(project_id: str, location: str, key_ring: str, crypto_key: str, key_version: str = "1") -> str:
    return f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{key_version}"


def crypto_key_path(project_id: str, location: str, key_ring: str, crypto_key: str) -> str:
    return f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}"
