import os
from google.cloud import kms_v1

# Google Cloud KMS client
kms_client = kms_v1.KeyManagementServiceClient()

# Config (env vars)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("KMS_LOCATION", "global")
KEY_RING_ID = os.getenv("KMS_KEY_RING")
KEY_ID = os.getenv("KMS_ENVELOPE_KEY")


def envelope_encrypt(plaintext: bytes) -> dict:
    """Perform envelope encryption: encrypt data with a symmetric DEK,
    then encrypt the DEK with a managed KMS key.

    Returns {
        "encrypted_data": base64_ciphertext,
        "encrypted_dek": base64_encrypted_key,
        "key_name": KMS key path used for DEK encryption
    }
    """
    # 1. Generate a random symmetric data encryption key (DEK)
    import base64, secrets

    dek = secrets.token_bytes(32)  # AES-256

    # 2. Encrypt plaintext with DEK (simple AES-256-GCM example; in production use a library)
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    encrypted_data = base64.b64encode(ct).decode()

    # 3. Encrypt the DEK using KMS
    key_path = kms_client.crypto_key_path(
        project=PROJECT_ID,
        location=LOCATION_ID,
        key_ring=KEY_RING_ID,
        crypto_key=KEY_ID,
    )
    kms_resp = kms_client.encrypt(name=key_path, plaintext=dek)
    encrypted_dek = base64.b64encode(kms_resp.ciphertext).decode()

    return {
        "encrypted_data": encrypted_data,
        "encrypted_dek": encrypted_dek,
        "key_name": key_path,
    }
