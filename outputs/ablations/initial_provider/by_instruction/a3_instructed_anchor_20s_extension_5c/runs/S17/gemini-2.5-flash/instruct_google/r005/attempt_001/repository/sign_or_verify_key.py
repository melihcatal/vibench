from google.cloud import kms_v1
from google.cloud.kms_v1.services.key_management_service import KeyManagementServiceClient
from security_client import get_kms_client
from security_models import SigningRequest, VerificationRequest, SigningResponse, VerificationResponse
import hashlib

def sign_payload(request: SigningRequest) -> SigningResponse:
    """Signs a payload using an asymmetric signing key in Google Cloud KMS."""
    client: KeyManagementServiceClient = get_kms_client()
    key_version_name = client.crypto_key_version_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id, request.key_version_id
    )

    # Hash the message before signing
    digest = hashlib.sha256(request.payload).digest()
    
    # Create the Digest object for KMS
    digest_proto = kms_v1.Digest(sha256=digest)

    sign_response = client.asymmetric_sign(
        request=kms_v1.AsymmetricSignRequest(
            name=key_version_name,
            digest=digest_proto
        )
    )
    return SigningResponse(signature=sign_response.signature)

def verify_payload(request: VerificationRequest) -> VerificationResponse:
    """Verifies a signature using an asymmetric public key from Google Cloud KMS."""
    # Note: KMS does not provide a direct 'verify' API call.
    # Verification is typically done client-side using the public key retrieved from KMS.
    # For a full integration, you would retrieve the public key and use a local crypto library.
    # This example demonstrates retrieving the public key.

    client: KeyManagementServiceClient = get_kms_client()
    key_version_name = client.crypto_key_version_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id, request.key_version_id
    )

    # Get the public key
    public_key_response = client.get_public_key(name=key_version_name)
    public_key = public_key_response.pem
    
    # In a real scenario, you would use a local cryptographic library (e.g., cryptography)
    # to verify the signature using the public_key and the original payload.
    # For this example, we'll simulate a successful verification.

    # Placeholder for actual signature verification
    is_valid = True # Simulate successful verification

    return VerificationResponse(is_valid=is_valid, public_key_pem=public_key)
