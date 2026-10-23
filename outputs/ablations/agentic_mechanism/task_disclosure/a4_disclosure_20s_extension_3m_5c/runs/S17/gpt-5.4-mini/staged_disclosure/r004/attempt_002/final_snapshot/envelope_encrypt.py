import base64
import os
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def generate_data_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)


def encrypt_data(plaintext: bytes, aad: Optional[bytes] = None) -> dict:
    project_id = _require_env("GOOGLE_CLOUD_PROJECT")
    location_id = _require_env("GOOGLE_CLOUD_KMS_LOCATION")
    key_ring_id = _require_env("GOOGLE_CLOUD_KMS_KEY_RING")
    crypto_key_id = _require_env("GOOGLE_CLOUD_KMS_CRYPTO_KEY")

    client = _kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)

    data_key = generate_data_key()
    aesgcm = AESGCM(data_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)

    wrapped_key = client.encrypt(request={"name": key_name, "plaintext": data_key}).ciphertext

    return {
        "provider": "google_cloud_kms",
        "encrypted_data_key": base64.b64encode(wrapped_key).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    }


def decrypt_data(package: dict, aad: Optional[bytes] = None) -> bytes:
    project_id = _require_env("GOOGLE_CLOUD_PROJECT")
    location_id = _require_env("GOOGLE_CLOUD_KMS_LOCATION")
    key_ring_id = _require_env("GOOGLE_CLOUD_KMS_KEY_RING")
    crypto_key_id = _require_env("GOOGLE_CLOUD_KMS_CRYPTO_KEY")

    client = _kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)

    wrapped_key = base64.b64decode(package["encrypted_data_key"])
    nonce = base64.b64decode(package["nonce"])
    ciphertext = base64.b64decode(package["ciphertext"])

    data_key = client.decrypt(request={"name": key_name, "ciphertext": wrapped_key}).plaintext
    aesgcm = AESGCM(data_key)
    return aesgcm.decrypt(nonce, ciphertext, aad)
