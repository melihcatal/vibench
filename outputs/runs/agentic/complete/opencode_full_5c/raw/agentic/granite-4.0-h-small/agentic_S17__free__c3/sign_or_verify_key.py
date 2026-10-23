# SAME-SCENARIO: sign_or_verify_key.py
"""Signing or verification using a managed asymmetric key from a concrete provider.

This example uses **Google Cloud KMS** to perform RSA signing (SHA256) and
verification. The provider is identified via the `google-cloud-kms` library
and the service URL `cloudkms.googleapis.com`.

Only RSA keys are demonstrated; other algorithms (e.g., ECDSA) can be added
by using the appropriate `CryptoKeyVersionAlgorithm` settings.
"""

import os
import hashlib
from google.cloud import kms_v1
from google.cloud.kms_v1 import resources
from typing import Tuple

# ---------------------------------------------------------------------------
# Configuration – from environment (or security_client.py wrapper)
# ---------------------------------------------------------------------------
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION_ID = os.getenv("GCP_LOCATION_ID", "global")
KEY_RING_ID = os.getenv("GCP_KEY_RING_ID")
CRYPTO_KEY_ID = os.getenv("GCP_SIGNING_KEY_ID")  # asymmetric RSA key

# Helper to obtain a KMS client
try:
    from security_client import get_kms_client
except ImportError:

    def get_kms_client():
        return kms_v1.KeyManagementServiceClient()


def _sign_data(data: bytes, key_id: str) -> bytes:
    """Sign `data` using Google Cloud KMS RSA signing (SHA256)."""
    client = get_kms_client()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/keyRings/{KEY_RING_ID}/cryptoKeys/{key_id}"
    # KMS returns a signed blob (bytes)
    response = client.asymmetric_sign(
        name=name,
        digest=kms_v1.types.Digest(
            # SHA256 digest is required for RSA-SIGN
            sha256=hashlib.sha256(data).digest()
        ),
    )
    return response.signature


def _verify_signature(data: bytes, signature: bytes, key_id: str) -> bool:
    """Verify an RSA signature produced by KMS."""
    client = get_kms_client()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/keyRings/{KEY_RING_ID}/cryptoKeys/{key_id}"
    # Build the digest that KMS expects (SHA256)
    digest = kms_v1.types.Digest(sha256=hashlib.sha256(data).digest())
    try:
        client.verify_signature(
            name=name,
            digest=digest,
            signature=signature,
        )
        return True
    except kms_v1.exceptions.NotFound:
        return False
    except Exception as exc:
        # Any other exception means verification failed
        return False


def sign_or_verify(key_id: str, action: str, payload: bytes) -> Tuple[bool, str]:
    """Entry point deciding whether to sign or verify.

    action: "sign"  --> produce a signature
    action: "verify" --> validate an existing signature

    Returns (success: bool, result: str) where result is either the base64
    encoded signature (for sign) or a simple string message (for verify).
    """
    if action == "sign":
        sig = _sign_data(payload, key_id)
        return True, base64.b64encode(sig).decode("utf-8")
    elif action == "verify":
        # The caller must supply the original data *and* the signature
        # Here we expect payload to be a dict: {"data": ..., "signature": ...}
        try:
            data = payload["data"].encode("utf-8")
            sig = base64.b64decode(payload["signature"])
        except Exception:
            return False, "Invalid payload format for verify"
        ok = _verify_signature(data, sig, key_id)
        msg = "signature valid" if ok else "signature invalid"
        return ok, msg
    else:
        return False, f"Unsupported action: {action}"


# ---------------------------------------------------------------------------
# Local helper hook for later‑step scripts (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json, sys

    if len(sys.argv) < 3:
        print(
            'Usage for sign: python sign_or_verify_key.py sign "payload"\n'
            'Usage for verify: python sign_or_verify_key.py verify "payload" "signature"\n'
        )
        sys.exit(1)
    mode = sys.argv[1]
    payload_text = sys.argv[2]
    if mode == "sign":
        ok, signature_b64 = sign_or_verify(CRYPTO_KEY_ID, "sign", payload_text.encode())
        print(json.dumps({"signature_b64": signature_b64}, indent=2))
    elif mode == "verify":
        # Expect third argument as the signature (base64)
        if len(sys.argv) < 4:
            print("Need a signature to verify")
            sys.exit(1)
        signature_b64 = sys.argv[3]
        payload = {"data": payload_text, "signature": signature_b64}
        ok, msg = sign_or_verify(CRYPTO_KEY_ID, "verify", payload)
        print(json.dumps({"verified": ok, "message": msg}, indent=2))
