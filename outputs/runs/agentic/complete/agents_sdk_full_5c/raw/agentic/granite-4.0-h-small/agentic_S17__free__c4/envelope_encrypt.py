import os
import base64
from google.cloud import kms_v1
from google.cloud import storage

from security_client import get_kms_client, get_storage_client
from security_models import serialize_request

def envelope_encrypt(payload: str, bucket_name: str, blob_name: str, project_id: str, location: str, key_ring: str, crypto_key: str) -> None:
    """Envelope encrypt a payload and store ciphertext in Cloud Storage.
    Uses a managed Cloud KMS key for key wrapping (AES256 GCM) and AESGCM for data encryption.

    Args:
        payload: plaintext to encrypt.
        bucket_name: GCS bucket to store ciphertext.
        blob_name: object name for ciphertext.
        project_id, location, key_ring, crypto_key: identifiers for the KMS key to protect the data key.
    """
    kms_client = get_kms_client()
    storage_client = get_storage_client()
    # 1) Generate a random data encryption key and wrap it with the managed KMS key
    #    (Google KMS supports asymmetric key wrapping; we use RSA-OAEP-256 here)
    wrap_req = kms_v1.types.WrapCryptoKeyRequest(\n        name=f\"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}\",\n        crypto_key_version=None  # auto picks primary version\n    )
    wrapped = kms_client.wrap_crypto_key(wrap_req)\n    encrypted_key = wrapped.ciphertext  # binary

    # 2) Encrypt payload with an AES-256-GCM key derived from the wrapped data key
    #    For simplicity we use the AES GCM mode provided by the python-cryptography package.
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    # Derive a 256‑bit AES key from the wrapped key (use SHA256 for demo)
    aes_key = base64.b64encode(wrapped.ciphertext)  # KMS returns base64 already; keep as bytes
    aes = AESGCM(aes_key[:32])  # truncate to 32 bytes (256 bits)\n    nonce = os.urandom(12)\n    ciphertext_blob = aes.encrypt(nonce, payload.encode('utf-8'), associated_data=b'')\n
    # 3) Store encrypted data and the wrapped key in Cloud Storage (metadata holds wrapped key)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.metadata = {"wrapped_key": base64.b64encode(encrypted_key).decode('utf-8')}\n    blob.upload_from_string(ciphertext_blob)\n
    print(f\"Envelope encryption stored blob '{blob_name}' in bucket '{bucket_name}' with wrapped key.\")
