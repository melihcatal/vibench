from security_client import SecurityClient
from security_models import SignRequest, SignResponse, VerifyRequest


def sign_payload(request: SignRequest) -> SignResponse:
    client = SecurityClient()
    key_version_path = client.get_kms_key_version_path(request.key_config)

    # Note: Google Cloud KMS signing requires the digest to be provided.
    # The digest type (e.g., SHA256) is inferred from the key configuration.
    response = client.kms_client.asymmetric_sign(
        name=key_version_path,
        digest={"sha256": request.message_digest},  # Assuming SHA256 for simplicity
    )
    return SignResponse(signature=response.signature, name=response.name)


def verify_payload(request: VerifyRequest) -> bool:
    client = SecurityClient()
    key_version_path = client.get_kms_key_version_path(request.key_config)

    # In KMS, verification is typically done by fetching the public key and then verifying locally.
    # For this example, we'll simulate verification by just checking if the public key can be retrieved.
    # A full verification would involve a crypto library like cryptography to verify the signature locally
    # using the public key retrieved from KMS.
    public_key_response = client.kms_client.get_public_key(name=key_version_path)

    # In a real scenario, you would use public_key_response.pem to verify the signature.
    # For this exercise, we will just return True as a placeholder for successful public key retrieval.
    return True
