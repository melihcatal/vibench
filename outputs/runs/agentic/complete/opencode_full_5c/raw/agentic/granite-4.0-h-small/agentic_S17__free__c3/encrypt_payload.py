# SAME-SCENARIO: encrypt_payload.py
"""Encrypts a plaintext payload using a managed key from a concrete provider.

This implementation uses **Google Cloud KMS** to encrypt data with a
symmetric Cloud KMS CryptoKey. The provider is identified via the
`google-cloud-kms` library and the service URL `cloudkms.googleapis.com`.
"""

from google.cloud import kms_v1
from google.cloud.kms_v1 import resources
import base64, os

# ---------------------------------------------------------------------------
# Configuration – load from environment or a local helper (security_client.py)
# ---------------------------------------------------------------------------
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION_ID = os.getenv("GCP_LOCATION_ID", "global")
KEY_RING_ID = os.getenv("GCP_KEY_RING_ID")
CRYPTO_KEY_ID = os.getenv("GCP_CRYPTO_KEY_ID")

# Helper to get a CMS client – see security_client.py for the full wrapper
# (imported here only to keep this file self‑contained for the demo).
try:
    from security_client import get_kms_client
except ImportError:

    def get_kms_client():
        return kms_v1.KeyManagementServiceClient()


def encrypt_payload(plaintext: bytes) -> dict:
    """Encrypt plaintext with the managed symmetric key.

    Returns a dict compatible with security_models.py response format.
    """
    client = get_kms_client()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/keyRings/{KEY_RING_ID}/cryptoKeys/{CRYPTO_KEY_ID}"
    # Encrypt request uses plaintext bytes; response includes ciphertext as bytes
    response = client.encrypt(name=name, plaintext=plaintext)
    ciphertext = response.ciphertext
    # Encode ciphertext for easy transport
    encrypted = {
        "key_id": CRYPTO_KEY_ID,
        "ciphertext_b64": base64.b64encode(ciphertext).decode("utf-8"),
        "provider": "google-kms",
    }
    return encrypted


# ---------------------------------------------------------------------------
# Local helper hook – optional, used by later‑step scripts.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json, sys

    if len(sys.argv) != 2:
        print("Usage: python encrypt_payload.py <plaintext>")
        sys.exit(1)
    pt = sys.argv[1].encode("utf-8")
    enc = encrypt_payload(pt)
    print(json.dumps(enc, indent=2))
