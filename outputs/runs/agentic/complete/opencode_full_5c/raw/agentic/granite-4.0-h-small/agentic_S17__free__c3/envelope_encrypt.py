# SAME-SCENARIO: envelope_encrypt.py
"""Envelope encryption implementation using a managed symmetric key.

The data encryption key (DEK) is generated locally, encrypted with a
managed Google Cloud KMS key (the "envelope"), and both the encrypted DEK
and the plaintext payload are returned. This pattern allows payloads to be
encrypted with a key owned by a centralized KMS while keeping the heavy
encryption work client‑side.

Provider identification: uses `google-cloud-kms` and the KMS service URL
`cloudkms.googleapis.com`.
"""

import os
import base64
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from google.cloud import kms_v1
from google.cloud.kms_v1 import resources

# ---------------------------------------------------------------------------
# Configuration – load from env vars or security_client.py
# ---------------------------------------------------------------------------
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION_ID = os.getenv("GCP_LOCATION_ID", "global")
KEY_RING_ID = os.getenv("GCP_KEY_RING_ID")
CRYPTO_KEY_ID = os.getenv("GCP_CRYPTO_KEY_ID")  # this is the envelope key (AES)

# Helper to obtain a KMS client
try:
    from security_client import get_kms_client
except ImportError:

    def get_kms_client():
        return kms_v1.KeyManagementServiceClient()

# ---------------------------------------------------------------------------
# Core envelope functions
# ---------------------------------------------------------------------------


def _generate_random_key(size: int = 32) -> bytes:
    """Generate a cryptographically secure random key of `size` bytes.
    Default is 256 bits for AES‑256."""
    return secrets.token_bytes(size)


def _encrypt_with_kms(plaintext: bytes, envelope_key_id: str) -> str:
    """Encrypt data using Google Cloud KMS (envelope)."""
    client = get_kms_client()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/keyRings/{KEY_RING_ID}/cryptoKeys/{envelope_key_id}"
    response = client.encrypt(name=name, plaintext=plaintext)
    # KMS returns ciphertext as bytes; encode to base64 for transport
    return base64.b64encode(response.ciphertext).decode("utf-8")


def _decrypt_with_kms(ciphertext_b64: str, envelope_key_id: str) -> bytes:
    """Decrypt data using Google Cloud KMS (envelope)."""
    client = get_kms_client()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/keyRings/{KEY_RING_ID}/cryptoKeys/{envelope_key_id}"
    ciphertext = base64.b64decode(ciphertext_b64)
    response = client.decrypt(name=name, ciphertext=ciphertext)
    return response.plaintext


# ---------------------------------------------------------------------------
# Public envelope_encrypt API
# ---------------------------------------------------------------------------
def envelope_encrypt(plaintext: str, envelope_key_id: str = None) -> dict:
    """Encrypt a plaintext string using envelope encryption.

    Returns a dict with:
      - encrypted_dek: base64‑encoded encrypted DEK (AES‑256)
      - encrypted_payload: base64‑encoded ciphertext produced by KMS
      - provider: identifier of the concrete provider used
    """
    if envelope_key_id is None:
        envelope_key_id = os.getenv("GCP_ENVELOPE_KEY_ID", "default-envelope-key")

    # 1. Generate a new random DEK (AES‑256)
    dek = _generate_random_key(32)
    dek_b64 = base64.b64encode(dek).decode("utf-8")

    # 2. Encrypt the DEK with the managed KMS envelope key
    encrypted_dek = _encrypt_with_kms(dek, envelope_key_id)

    # 3. Encrypt the plaintext payload with the plaintext DEK (AES‑256 CBC)
    cipher = AES.new(dek, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    iv_b64 = base64.b64encode(cipher.iv).decode("utf-8")
    ct_b64 = base64.b64encode(ct_bytes).decode("utf-8")

    response = {
        "encrypted_dek": encrypted_dek,
        "iv": iv_b64,
        "payload": ct_b64,
        "provider": "google-kms-envelope",
    }
    return response


# ---------------------------------------------------------------------------
# Public envelope_decrypt API
# ---------------------------------------------------------------------------
def envelope_decrypt(envelope: dict, envelope_key_id: str = None) -> str:
    """Decrypt an envelope dict produced by envelope_encrypt().

    Returns the original plaintext string.
    """
    if envelope_key_id is None:
        envelope_key_id = os.getenv("GCP_ENVELOPE_KEY_ID", "default-envelope-key")

    # 1. Decrypt the DEK using KMS
    encrypted_dek_b64 = envelope["encrypted_dek"]
    encrypted_dek = base64.b64decode(encrypted_dek_b64)
    decrypted_dek = _decrypt_with_kms(encrypted_dek_b64, envelope_key_id)

    # 2. Decrypt the payload using the recovered DEK
    iv = base64.b64decode(envelope["iv"])
    ct = base64.b64decode(envelope["payload"])
    cipher = AES.new(decrypted_dek, AES.MODE_CBC, iv=iv)
    plaintext_bytes = unpad(cipher.decrypt(ct), AES.block_size)
    return plaintext_bytes.decode("utf-8")


# ---------------------------------------------------------------------------
# Local demo helper (optional, used by later‑step scripts)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json, sys

    if len(sys.argv) < 2:
        print("Usage: python envelope_encrypt.py <plaintext>")
        sys.exit(1)
    plain = sys.argv[1]
    env = envelope_encrypt(plain)
    print(json.dumps(env, indent=2))
