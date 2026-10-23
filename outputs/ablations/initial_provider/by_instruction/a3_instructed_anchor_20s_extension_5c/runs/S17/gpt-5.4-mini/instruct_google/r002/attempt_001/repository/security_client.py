import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import kms_v1


@dataclass
class SecurityConfig:
    project_id: str
    location: str
    key_ring: str
    crypto_key: str
    key_version: Optional[str] = None


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("GOOGLE_CLOUD_KMS_LOCATION", "global"),
        key_ring=os.environ["GOOGLE_CLOUD_KMS_KEY_RING"],
        crypto_key=os.environ["GOOGLE_CLOUD_KMS_CRYPTO_KEY"],
        key_version=os.environ.get("GOOGLE_CLOUD_KMS_KEY_VERSION"),
    )


def kms_key_name(config: SecurityConfig) -> str:
    return f"projects/{config.project_id}/locations/{config.location}/keyRings/{config.key_ring}/cryptoKeys/{config.crypto_key}"


def kms_key_version_name(config: SecurityConfig) -> str:
    if config.key_version:
        return f"{kms_key_name(config)}/cryptoKeyVersions/{config.key_version}"
    return kms_key_name(config)


def kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def decrypt_aead_ciphertext(ciphertext: bytes, plaintext_aad: bytes = b"") -> Dict[str, Any]:
    config = load_security_config()
    client = kms_client()
    response = client.decrypt(
        request={
            "name": kms_key_name(config),
            "ciphertext": ciphertext,
            "additional_authenticated_data": plaintext_aad,
        }
    )
    return {"plaintext": response.plaintext.decode("utf-8", errors="replace"), "key": kms_key_name(config)}
