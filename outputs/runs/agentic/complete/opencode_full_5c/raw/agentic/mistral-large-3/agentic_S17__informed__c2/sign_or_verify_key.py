from security_client import GoogleKMSClient
from security_models import normalize_signing_result, normalize_verification_result


def sign_or_verify_key(
    data: bytes,
    signature: bytes = None,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    key_id: str = None,
    action: str = "sign",
) -> dict:
    """
    Signs or verifies data using Google Cloud KMS.

    Args:
        data: The data bytes to sign or verify.
        signature: The signature bytes to verify. Required if action is "verify".
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
        location_id: Google Cloud location ID. Defaults to "global".
        key_ring_id: Google Cloud key ring ID. Defaults to GOOGLE_CLOUD_KEY_RING env var.
        key_id: Google Cloud key ID. Defaults to GOOGLE_CLOUD_KEY_ID env var.
        action: Either "sign" or "verify". Defaults to "sign".

    Returns:
        Dictionary containing signature (if signing), valid (if verifying), key_version, provider, and success status.
    """
    client = GoogleKMSClient(project_id, location_id, key_ring_id, key_id)

    if action == "sign":
        result = client.sign(data)
        return normalize_signing_result(result).__dict__
    elif action == "verify":
        if not signature:
            return normalize_verification_result(
                {
                    "error": "Signature is required for verification",
                    "provider": "google_cloud_kms",
                    "success": False,
                }
            ).__dict__
        result = client.verify(data, signature)
        return normalize_verification_result(result).__dict__
    else:
        return normalize_verification_result(
            {
                "error": "Invalid action. Use 'sign' or 'verify'",
                "provider": "google_cloud_kms",
                "success": False,
            }
        ).__dict__
