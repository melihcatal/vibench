# [SAME-SCENARIO] envelope_encrypt.py
# Implements envelope encryption using Google Cloud KMS
from google.cloud import kms_v1
import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from security_client import kms_client_from_config


def envelope_encrypt(
    project_id, location_id, key_ring_id, crypto_key_id, plaintext: bytes
) -> dict:
    """Encrypts data using envelope encryption (data key + KMS-wrapped key).

    Returns a dict with:
        - ciphertext: encrypted payload
        - data_key: base64-encoded random data key used for payload encryption
        - wrapped_key: base64-encoded KMS-wrapped data key
    Uses Google Cloud KMS as the concrete KMS provider.
    """
    # Generate a random 256‑bit data key
    data_key = get_random_bytes(32)
    # Encrypt the plaintext with the data key (AES‑GCM)
    cipher = AES.new(data_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    # Wrap the data key with the managed KMS key
    client = kms_v1.KeyManagementServiceClient()
    # client = kms_client_from_config()  # could be used for configured client
    name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    wrap_response = client.encrypt(name, base64.b64encode(data_key).decode("utf-8"))
    wrapped_key = wrap_response.ciphertext  # already base64‑encoded by KMS
    # Return combined envelope
    return {
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "iv": base64.b64encode(cipher.nonce).decode("utf-8"),
        "wrapped_key": wrapped_key,
        "tag": base64.b64encode(tag).decode("utf-8"),
    }


if __name__ == "__main__":
    # Example usage – replace placeholders with real config values
    project = os.getenv("KMS_PROJECT_ID")
    location = os.getenv("KMS_LOCATION_ID")
    ring = os.getenv("KMS_KEY_RING_ID")
    key = os.getenv("KMS_CRYPTO_KEY_ID")
    data = b"Secret payload for envelope encryption"
    envelope = envelope_encrypt(project, location, ring, key, data)
    print("Envelope:", envelope)
