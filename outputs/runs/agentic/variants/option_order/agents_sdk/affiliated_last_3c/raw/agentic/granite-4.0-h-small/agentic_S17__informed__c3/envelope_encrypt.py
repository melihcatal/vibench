# [SAME-SCENARIO] envelope_encrypt.py

import os
from google.cloud import kms_v1

# Helper utilities and client configuration are imported from local modules.
from security_client import KmsClient
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(plaintext: str, kms_key_name: str) -> EnvelopeEncryptResponse:
    """Perform envelope encryption using Google Cloud KMS.

    1. Generate a random data encryption key (DEK).
    2. Encrypt the DEK with the KMS key (envelope).
    3. Encrypt the plaintext with the plaintext DEK.
    4. Return both the encrypted DEK and the DEK‑encrypted data.

    Args:
        plaintext (str): The data to encrypt.
        kms_key_name (str): Full resource name of the KMS CryptoKey.

    Returns:
        EnvelopeEncryptResponse: envelope_encrypted_data and encrypted_dek.
    """
    # Generate a random 256‑bit DEK (local to this function).
    dek = os.urandom(32)
    # Encrypt the plaintext with the plaintext DEK (simple AES‑GCM performed locally).
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    auth_tag = encryptor.tag
    encrypted_data = iv + ciphertext + auth_tag

    # Encrypt the DEK with the KMS key using the KmsClient (reads env vars for authentication).
    client = KmsClient()
    envelope_resp = client.encrypt(EncryptRequest(key_name=kms_key_name, plaintext=dek.hex()))
    encrypted_dek = envelope_resp.ciphertext  # already base64‑encoded

    return EnvelopeEncryptResponse(
        encrypted_dek=encrypted_dek,
        encrypted_data=encrypted_data,
        iv=iv,
        auth_tag=auth_tag,
    )


if __name__ == "__main__":
    # Simple demo of envelope encryption.
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_KMS_LOCATION", "global")
    key_ring = os.getenv("GCP_KMS_KEY_RING")
    crypto_key = os.getenv("GCP_KMS_CRYPTO_KEY")
    plaintext = "Sensitive business data"
    kms_key_name = f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}"
    envelope = envelope_encrypt(plaintext, kms_key_name)

    print("Encrypted DEK (base64):", envelope.encrypted_dek)
    print("Encrypted data (hex):", envelope.encrypted_data.hex())
