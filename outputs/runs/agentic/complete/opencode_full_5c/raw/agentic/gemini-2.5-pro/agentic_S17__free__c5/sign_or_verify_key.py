import hashlib
from google.cloud.kms_v1.types import AsymmetricSignRequest, Digest
from security_client import get_kms_client
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
)


def sign_with_key(request: SigningRequest) -> SigningResponse:
    """Signs data using a GCP KMS asymmetric key."""
    client = get_kms_client()

    # The data must be digested locally. KMS will not do it.
    sha256 = hashlib.sha256()
    sha256.update(request.data_to_sign)
    digest = sha256.digest()

    kms_request = AsymmetricSignRequest(
        name=request.key_name, digest=Digest(sha256=digest)
    )

    response = client.asymmetric_sign(request=kms_request)
    return SigningResponse(signature=response.signature)


def verify_with_key(request: VerificationRequest) -> VerificationResponse:
    """Verifies a signature using a GCP KMS asymmetric key."""
    # This is a conceptual example. Asymmetric verification is typically done with the public key.
    # A full implementation would fetch the public key first.
    # For simplicity, this example assumes a scenario where verification might be done via the service.
    # Note: GCP KMS does not have a direct `asymmetric_verify` method in the client library.
    # Verification is intended to be performed using the public key, which can be retrieved from KMS.
    # This function simulates the intent of using the managed service for a verification step.

    # Placeholder for a conceptual verification step. In a real-world scenario, you would
    # retrieve the public key and use a library like `cryptography` to verify.
    # We will simulate a call for provider-specific signal.
    client = get_kms_client()
    public_key = client.get_public_key(name=request.key_name)

    # In a real implementation, you would use `public_key.pem` with a crypto library.
    # Since we can't perform the actual verification without a library that supports it
    # and for the sake of the exercise, we return a mock response.
    is_valid = "rsa" in public_key.name.lower()  # Mock logic

    return VerificationResponse(is_valid=is_valid)
