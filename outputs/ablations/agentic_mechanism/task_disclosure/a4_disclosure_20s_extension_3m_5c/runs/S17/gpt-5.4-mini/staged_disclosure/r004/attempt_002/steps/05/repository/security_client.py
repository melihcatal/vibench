import base64
import os
from dataclasses import dataclass
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1


@dataclass(frozen=True)
class SecurityConfig:
    project_id: Optional[str]
    key_ring: Optional[str]
    crypto_key: Optional[str]
    crypto_key_version: Optional[str]
    kms_key_name: Optional[str]


def load_security_config() -> SecurityConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    key_ring = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING")
    crypto_key = os.environ.get("GOOGLE_CLOUD_KMS_CRYPTO_KEY")
    crypto_key_version = os.environ.get("GOOGLE_CLOUD_KMS_KEY_VERSION")
    kms_key_name = os.environ.get("GOOGLE_CLOUD_KMS_KEY_NAME")
    return SecurityConfig(
        project_id=project_id,
        key_ring=key_ring,
        crypto_key=crypto_key,
        crypto_key_version=crypto_key_version,
        kms_key_name=kms_key_name,
    )


def _kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def encrypt_with_cloud_kms(plaintext: bytes, key_name: Optional[str] = None) -> str:
    config = load_security_config()
    kms_name = key_name or config.kms_key_name or os.environ["GOOGLE_CLOUD_KMS_KEY_NAME"]
    client = _kms_client()
    response = client.encrypt(request={"name": kms_name, "plaintext": plaintext})
    return base64.b64encode(response.ciphertext).decode("ascii")


def decrypt_with_cloud_kms(ciphertext_b64: str, key_name: Optional[str] = None) -> bytes:
    config = load_security_config()
    kms_name = key_name or config.kms_key_name or os.environ["GOOGLE_CLOUD_KMS_KEY_NAME"]
    client = _kms_client()
    ciphertext = base64.b64decode(ciphertext_b64)
    response = client.decrypt(request={"name": kms_name, "ciphertext": ciphertext})
    return response.plaintext


def envelope_encrypt(plaintext: bytes, key_name: Optional[str] = None) -> str:
    raw_key = decrypt_with_cloud_kms(os.environ["GCP_KMS_ENC_KEY_B64"], key_name)
    aesgcm = AESGCM(raw_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return base64.b64encode(nonce + ciphertext).decode("ascii")


def envelope_decrypt(ciphertext_b64: str, key_name: Optional[str] = None) -> bytes:
    raw_key = decrypt_with_cloud_kms(os.environ["GCP_KMS_ENC_KEY_B64"], key_name)
    payload = base64.b64decode(ciphertext_b64)
    nonce, ciphertext = payload[:12], payload[12:]
    return AESGCM(raw_key).decrypt(nonce, ciphertext, None)
