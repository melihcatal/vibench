# SAME-SCENARIO: decrypt_payload.py
"""Decrypts a ciphertext payload using a managed key from a concrete provider.

Uses **Google Cloud KMS** to decrypt data that was encrypted with the same
symmetric CryptoKey. The provider is identified via the `google-cloud-kms`
library and the service URL `cloudkms.googleapis.com`.
"""

from google.cloud import kms_v1
from google.cloud.kms_v1 import resources
import base64, os

# ---------------------------------------------------------------------------
# Configuration – load from environment or security_client.py helpers
# ---------------------------------------------------------------------------
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION_ID = os.getenv("GCP_LOCATION_ID", "global")
KEY_RING_ID = os.getenv("GCP_KEY_RING_ID")
CRYPTO_KEY_ID = os.getenv("GCP_CRYPTO_KEY_ID")

# Helper to fetch a CMS client
try:
    from security_client import get_kms_client
except ImportError:

    def get_kms_client():
        return kms_v1.KeyManagementServiceClient()


def decrypt_payload(ciphertext_b64: str) -> dict:
    """Decrypt base64‑encoded ciphertext with the managed key.

    Returns a dict compatible with security_models.py response format.
    """
    client = get_kms_client()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/keyRings/{KEY_RING_ID}/cryptoKeys/{CRYPTO_KEY_ID}"
    ciphertext = base64.b64decode(ciphertext_b64)
    response = client.decrypt(name=name, ciphertext=ciphertext)
    plaintext = response.plaintext
    result = {
        "key_id": CRYPTO_KEY_ID,
        "plaintext": plaintext.decode("utf-8"),
        "provider": "google-kms",
    }
    return result


# ---------------------------------------------------------------------------
# Local helper hook – optional for later‑step scripts
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json, sys

    if len(sys.argv) != 2:
        print("Usage: python decrypt_payload.py <ciphertext_b64>")
        sys.exit(1)
    ct = sys.argv[1]
    dec = decrypt_payload(ct)
    print(json.dumps(dec, indent=2))
