# [SAME-SCENARIO] sign_or_verify_key.py

import os
from google.cloud import kms_v1

# Helper utilities and client configuration are imported from local modules.
from security_client import KmsClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_data(data: bytes, kms_key_name: str) -> SignResponse:
    """Sign data using a Google Cloud KMS asymmetric key (RSA/ECDSA).

    Args:
        data (bytes): Raw data to be signed.
        kms_key_name (str): Full resource name of an asymmetric KMS CryptoKey.

    Returns:
        SignResponse: The signature (base64‑encoded).
    """
    client = KmsClient()
    # Google KMS returns the signature as a ByteString; we convert to base64.
    resp = client.sign(SignRequest(key_name=kms_key_name, data=data))
    return SignResponse(signature=resp.signature.decode('utf-8'))


def verify_signature(data: bytes, signature: str, kms_key_name: str) -> VerifyResponse:
    """Verify a signature produced by the same KMS asymmetric key.

    Args:
        data (bytes): Original data that was signed.
        signature (str): Base64‑encoded signature to verify.
        kms_key_name (str): Full resource name of the asymmetric KMS CryptoKey.

    Returns:
        VerifyResponse: True if verification succeeds.
    """
    client = KmsClient()
    resp = client.verify(
        VerifyRequest(
            key_name=kms_key_name,
            data=data,
            signature=signature.encode('utf-8'),
        )
    )
    return VerifyResponse(is_valid=resp.success)


if __name__ == "__main__":
    # Demo using an RSA 2048‑bit key for signing SHA256.
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_KMS_LOCATION", "global")
    key_ring = os.getenv("GCP_KMS_KEY_RING")
    crypto_key = os.getenv("GCP_KMS_SIGN_KEY")  # an asymmetric key
    kms_key_name = f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}"

    sample_data = b"Document to be signed"
    signature = sign_data(sample_data, kms_key_name).signature
    print("Signature (base64):", signature)

    # Verify the signature.
    is_valid = verify_signature(sample_data, signature, kms_key_name).is_valid
    print("Signature verification result:", is_valid)
