# [SAME-SCENARIO] sign_or_verify_key.py
# Uses Google Cloud KMS for signing and verification where supported

from google.cloud import kms_v1

client = kms_v1.KeyManagementServiceClient()


def sign_key(project_id, location_id, key_ring_id, crypto_key_id, data):
    """Signs data using a Cloud KMS asymmetric signing key.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Cloud location (e.g., "us-central1").
        key_ring_id (str): KMS key ring identifier.
        crypto_key_id (str): KMS crypto key identifier (must support signing).
        data (bytes): Data to sign.

    Returns:
        dict: Signature and metadata.
    """
    key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    response = client.sign_asymmetric_sign(name=key_name, data=data)
    return {
        "signature": response.signature,
        "algorithm": response.algorithm,
    }


def verify_signature(
    project_id, location_id, key_ring_id, crypto_key_id, signature, data
):
    """Verifies a signature produced by sign_key using Cloud KMS.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Cloud location (e.g., "us-central1").
        key_ring_id (str): KMS key ring identifier.
        crypto_key_id (str): KMS crypto key identifier (must support signing).
        signature (bytes): Signature to verify.
        data (bytes): Original data that was signed.

    Returns:
        bool: True if verification succeeds, False otherwise.
    """
    key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    try:
        client.verify_asymmetric_verify(name=key_name, signature=signature, data=data)
        return True
    except Exception:
        return False
