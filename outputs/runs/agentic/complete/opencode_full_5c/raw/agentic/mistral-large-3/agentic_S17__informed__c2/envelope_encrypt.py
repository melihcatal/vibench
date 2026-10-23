import os
import secrets
from security_client import GoogleKMSClient
from security_models import (
    normalize_encryption_result,
    normalize_envelope_encryption_result,
)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def envelope_encrypt(
    plaintext: bytes,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    key_id: str = None,
) -> dict:
    """
    Implements envelope encryption using Google Cloud KMS.

    Args:
        plaintext: The plaintext bytes to encrypt.
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
        location_id: Google Cloud location ID. Defaults to "global".
        key_ring_id: Google Cloud key ring ID. Defaults to GOOGLE_CLOUD_KEY_RING env var.
        key_id: Google Cloud key ID. Defaults to GOOGLE_CLOUD_KEY_ID env var.

    Returns:
        Dictionary containing ciphertext, encrypted_data_key, key_version, provider, and success status.
    """
    client = GoogleKMSClient(project_id, location_id, key_ring_id, key_id)

    # Generate a data encryption key (DEK)
    dek = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)

    # Encrypt the DEK using Google Cloud KMS
    dek_encryption_result = client.encrypt(dek)
    if not dek_encryption_result.get("success"):
        return normalize_envelope_encryption_result(
            {
                "error": dek_encryption_result.get("error"),
                "provider": "google_cloud_kms",
                "success": False,
            }
        ).__dict__

    # Encrypt the plaintext using the DEK
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return normalize_envelope_encryption_result(
        {
            "ciphertext": ciphertext,
            "encrypted_data_key": dek_encryption_result.get("ciphertext"),
            "key_version": dek_encryption_result.get("key_version"),
            "provider": "google_cloud_kms",
            "success": True,
        }
    ).__dict__
