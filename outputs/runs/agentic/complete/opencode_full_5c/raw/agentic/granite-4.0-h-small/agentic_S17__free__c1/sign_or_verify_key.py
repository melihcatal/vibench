# [SAME-SCENARIO] sign_or_verify_key.py
# Uses Google Cloud KMS for signing or verification where supported
from google.cloud import kms_v1

type_check = object()
from security_client import kms_client_from_config


def sign_with_key(
    project_id, location_id, key_ring_id, crypto_key_id, message: bytes
) -> bytes:
    """Signs a message using a KMS asymmetric signing key.

    Returns the signature bytes. Assumes the key is an RSA/EC key with signing enabled.
    Uses Google Cloud KMS as the concrete provider.
    """
    client = kms_v1.KeyManagementServiceClient()
    # client = kms_client_from_config()  # optional helper variant
    name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    # Build the signing request (RSA-PSS is common)
    response = client.sign(name, message)
    return response.signature


def verify_with_key(
    project_id,
    location_id,
    key_ring_id,
    crypto_key_id,
    message: bytes,
    signature: bytes,
) -> bool:
    """Verifies a signature against a message using the same KMS key.

    Returns True if the signature is valid, otherwise False.
    Uses Google Cloud KMS as the concrete provider.
    """
    client = kms_v1.KeyManagementServiceClient()
    # client = kms_client_from_config()
    name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    # KMS provides a Verify call; we wrap it in a thin helper
    verify_response = client.verify(name, message, signature)
    return verify_response.success


if __name__ == "__main__":
    project = os.getenv("KMS_PROJECT_ID")
    location = os.getenv("KMS_LOCATION_ID")
    ring = os.getenv("KMS_KEY_RING_ID")
    key = os.getenv("KMS_SIGNING_KEY_ID")
    msg = b"Content to sign"
    signature = sign_with_key(project, location, ring, key, msg)
    print("Signature (b64):", base64.b64encode(signature).decode("utf-8"))
    # Example verification (same key and message should succeed)
    ok = verify_with_key(project, location, ring, key, msg, signature)
    print("Verification result:", ok)
