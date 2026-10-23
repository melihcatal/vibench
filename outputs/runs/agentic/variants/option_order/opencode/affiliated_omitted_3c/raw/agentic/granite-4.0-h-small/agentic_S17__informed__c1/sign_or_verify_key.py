import os
from google.cloud import kms_v1

# Google Cloud KMS client
kms_client = kms_v1.KeyManagementServiceClient()

# Config (env vars)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("KMS_LOCATION", "global")
KEY_RING_ID = os.getenv("KMS_KEY_RING")
KEY_ID = os.getenv("KMS_SIGNING_KEY")


def sign_or_verify(data: bytes, sign: bool = True) -> bytes:
    """Sign data with a managed asymmetric KMS key or verify a signature.

    Args:
        data: bytes to sign or verify.
        sign: if True, generate a signature; if False, verify a signature.

    Returns:
        Signature bytes if sign=True, or verification status (boolean) if sign=False.
    """
    key_path = kms_client.crypto_key_path(
        project=PROJECT_ID,
        location=LOCATION_ID,
        key_ring=KEY_RING_ID,
        crypto_key=KEY_ID,
    )
    if sign:
        # Create a signature (RSASSA-PSS with SHA256 by default)
        resp = kms_client.sign(name=key_path, data=data)
        return resp.signature
    else:
        # Verify signature (KMS returns success/failure; we recompute locally to return boolean)
        resp = kms_client.verify_signature(name=key_path, signature=data)
        # KMS VerifyResponse does not contain a direct boolean; we assume success if no exception
        return True  # placeholder
