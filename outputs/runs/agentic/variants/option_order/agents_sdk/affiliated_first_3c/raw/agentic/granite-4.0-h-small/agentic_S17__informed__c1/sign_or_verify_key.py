import os
from google.cloud import kms
from security_client import get_kms_client

def sign_key(project_id, location_id, key_ring_id, crypto_key_id, message, kms_client=None):
    """Signs a message using a Google Cloud KMS asymmetric key (signing capability). 
    Returns the signature (bytes). Uses RSA-PSS or ECDSA as supported by the key.
    """
    if kms_client is None:
        kms_client = get_kms_client()
    key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    response = kms_client.asymmetric_sign(
        name=key_name,
        digest={
            "sha256": message,
        },
    )
    return response.signature


def verify_key(project_id, location_id, key_ring_id, crypto_key_id, message, signature, kms_client=None):
    """Verifies a signature using the same KMS asymmetric key (verification capability). 
    Returns True if verification succeeds.
    """
    if kms_client is None:
        kms_client = get_kms_client()
    key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    try:
        kms_client.verify_signature(
            name=key_name,
            digest={"sha256": message},
            signature=signature,
        )
        return True
    except Exception as e:
        # In production inspect e for specific error details
        print("Verification failed:", e)
        return False

if __name__ == "__main__":
    # Example usage (requires an asymmetric signing key in KMS)
    project_id = os.getenv("GCLOUD_PROJECT")
    location_id = "global"
    key_ring_id = "my-key-ring"
    crypto_key_id = "my-signing-key"
    msg = b"Data to sign"
    signature = sign_key(project_id, location_id, key_ring_id, crypto_key_id, msg)
    print("Signature (base64):", signature)
    # Verify
    success = verify_key(project_id, location_id, key_ring_id, crypto_key_id, msg, signature)
    print("Verification OK?", success)
