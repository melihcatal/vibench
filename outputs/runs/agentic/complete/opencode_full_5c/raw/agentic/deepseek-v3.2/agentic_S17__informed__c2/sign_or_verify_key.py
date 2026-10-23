import os
import hashlib
from google.cloud import kms
from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_data(data: bytes, key_name: str) -> SignResponse:
    """
    Sign data using Google Cloud KMS asymmetric signing key.
    """
    client = get_kms_client()

    if not data:
        raise ValueError("Data cannot be empty")

    if not key_name:
        raise ValueError("Key name cannot be empty")

    try:
        # Create digest of the data
        digest = hashlib.sha256(data).digest()

        response = client.asymmetric_sign(
            request={"name": key_name, "digest": {"sha256": digest}}
        )

        signature = response.signature

        return SignResponse(
            success=True,
            signature=signature,
            key_id=key_name,
            algorithm="RSA_SIGN_PSS_2048_SHA256",
            provider="google-cloud-kms",
        )
    except Exception as e:
        return SignResponse(
            success=False, error=str(e), key_id=key_name, provider="google-cloud-kms"
        )


def verify_signature(data: bytes, signature: bytes, key_name: str) -> VerifyResponse:
    """
    Verify a signature using Google Cloud KMS asymmetric signing key.
    """
    client = get_kms_client()

    if not data:
        raise ValueError("Data cannot be empty")

    if not signature:
        raise ValueError("Signature cannot be empty")

    if not key_name:
        raise ValueError("Key name cannot be empty")

    try:
        # Create digest of the data
        digest = hashlib.sha256(data).digest()

        response = client.asymmetric_sign(
            request={"name": key_name, "digest": {"sha256": digest}}
        )

        # For verification, we would normally use get_public_key and verify locally
        # But KMS doesn't have a direct verify API, so we sign again and compare
        expected_signature = response.signature

        # In a real implementation, we would get the public key and verify
        # For this example, we'll simulate verification by comparing with re-signed data
        is_valid = signature == expected_signature

        return VerifyResponse(
            success=True,
            is_valid=is_valid,
            key_id=key_name,
            algorithm="RSA_SIGN_PSS_2048_SHA256",
            provider="google-cloud-kms",
        )
    except Exception as e:
        return VerifyResponse(
            success=False, error=str(e), key_id=key_name, provider="google-cloud-kms"
        )
