import os
from google.cloud import kms
from security_client import get_kms_client, generate_data_encryption_key

def envelope_encrypt(plaintext, master_key_name, kms_client=None):
    """Envelopes plaintext: encrypts it with a data encryption key (DEK) and encrypts the DEK with master_key_name.
    Returns ciphertext (bytes) and the encrypted DEK (bytes).
    Uses Google Cloud KMS for envelope encryption.
    """
    if kms_client is None:
        kms_client = get_kms_client()
    # 1. Generate a random DEK (e.g., AES-256-GCM)
    dek = generate_data_encryption_key(32)  # 32 bytes = 256 bits
    # 2. Encrypt the plaintext with the DEK using AES-GCM (local)
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    # 3. Encrypt the DEK with the managed KMS key (Google Cloud KMS)
    response = kms_client.encrypt(
        name=master_key_name,
        plaintext=dek,
        additional_authenticated_data=b"EnvelopeWrap",
    )
    encrypted_dek = response.ciphertext
    return ct, encrypted_dek, nonce

if __name__ == "__main__":
    # Example usage (credentials via GOOGLE_APPLICATION_CREDENTIALS)
    project_id = os.getenv("GCLOUD_PROJECT")
    location_id = "global"
    key_ring_id = "my-key-ring"
    crypto_key_id = "my-master-key"
    master_key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    plaintext = b"Sensitive data to protect"
    ct, edek, nonce = envelope_encrypt(plaintext, master_key_name)
    print("Ciphertext (base64):", ct)
    print("Encrypted DEK (base64):", edek)
