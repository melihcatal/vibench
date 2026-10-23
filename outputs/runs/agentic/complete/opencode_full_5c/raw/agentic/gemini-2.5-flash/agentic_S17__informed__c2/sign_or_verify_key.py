from google.cloud import kms_v1
from google.cloud.kms_v1 import types
from security_client import get_kms_client, get_key_version_path
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
)
import os
import base64
import hashlib


def sign_data(request: SigningRequest) -> SigningResponse:
    """Signs a data payload using an asymmetric signing key in Google Cloud KMS.

    Args:
        request: A SigningRequest object containing the data to sign and the KMS key version ID.
                 The key_id in the request should be the full crypto key version path.

    Returns:
        A SigningResponse object with the signature and key ID.
    """
    kms_client = get_kms_client()

    # The key_id in the request should be the full resource name of the CryptoKeyVersion.
    full_key_version_path = request.key_id

    # Prepare the data for signing by taking its SHA256 hash
    data_bytes = request.data.encode("utf-8")
    digest = hashlib.sha256(data_bytes).digest()

    # Create a Digest object required by the asymmetric_sign method
    digest_proto = types.Digest(sha256=digest)

    try:
        # Call the KMS API to sign the data
        response = kms_client.asymmetric_sign(
            name=full_key_version_path, digest=digest_proto
        )

        # The signature is returned as bytes, encode it to base64 for string representation
        signature_b64 = base64.b64encode(response.signature)

        return SigningResponse(signature=signature_b64, key_id=request.key_id)
    except Exception as e:
        raise RuntimeError(f"Error signing data with Google Cloud KMS: {e}")


def verify_signature(request: VerificationRequest) -> VerificationResponse:
    """Verifies a signature using an asymmetric public key from Google Cloud KMS.

    Args:
        request: A VerificationRequest object containing the data, signature, and KMS key version ID.
                 The key_id in the request should be the full crypto key version path.

    Returns:
        A VerificationResponse object indicating if the signature is valid and the key ID.
    """
    kms_client = get_kms_client()

    # The key_id in the request should be the full resource name of the CryptoKeyVersion.
    full_key_version_path = request.key_id

    # First, get the public key associated with the key version
    try:
        public_key_response = kms_client.get_public_key(name=full_key_version_path)
        public_key_pem = public_key_response.pem.encode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Error retrieving public key from Google Cloud KMS: {e}")

    # Prepare the data for verification by taking its SHA256 hash
    data_bytes = request.data.encode("utf-8")
    digest = hashlib.sha256(data_bytes).digest()

    # For local verification using cryptography library
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization
    from cryptography.exceptions import InvalidSignature

    try:
        public_key = serialization.load_pem_public_key(public_key_pem)

        # Decode the base64 signature back to bytes
        signature_bytes = base64.b64decode(request.signature)

        # Verify the signature locally using the public key
        # The padding and algorithm should match what was used for signing in KMS.
        # For RSA PSS, it's usually padding.PSS and hashes.SHA256
        # For RSA PKCS1v15, it's usually padding.PKCS1v15 and hashes.SHA256
        # Assuming RSA_SIGN_PSS_2048_SHA256, RSA_SIGN_PSS_3072_SHA256, etc. which uses PSS padding
        public_key.verify(
            signature_bytes,
            data_bytes,  # KMS asymmetric_sign takes digest, but verify_signature here uses original data and then computes digest internally
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        is_valid = True
    except InvalidSignature:
        is_valid = False
    except Exception as e:
        raise RuntimeError(f"Error verifying signature: {e}")

    return VerificationResponse(is_valid=is_valid, key_id=request.key_id)
