import base64
from google.cloud import kms
from google.protobuf import wrappers_pb2
from security_models import SignVerifyRequest, SignVerifyResponse
from security_client import KmsClient
import hashlib

def sign_payload(request: SignVerifyRequest) -> SignVerifyResponse:
    kms_client = KmsClient()
    client = kms_client.client

    key_version_name = kms_client.get_key_version_path(
        request.project_id, request.location, request.key_ring, request.key_id, request.version_id
    )

    # Hash the message before signing
    sha256 = hashlib.sha256(request.message.encode('utf-8'))
    digest = wrappers_pb2.BytesValue(value=sha256.digest())

    sign_response = client.asymmetric_sign(
        request={"name": key_version_name, "digest": {"sha256": digest}}
    )
    return SignVerifyResponse(result=True, signature=sign_response.signature)

def verify_signature(request: SignVerifyRequest) -> SignVerifyResponse:
    kms_client = KmsClient()
    client = kms_client.client

    key_version_name = kms_client.get_key_version_path(
        request.project_id, request.location, request.key_ring, request.key_id, request.version_id
    )

    # Get the public key for verification
    public_key_response = client.get_public_key(request={"name": key_version_name})
    # In a real scenario, you'd use a crypto library to verify the signature using the public_key_response.pem
    # For this example, we'll just simulate a verification.

    # Decode the base64 encoded signature from the request
    signature_bytes = base64.b64decode(request.signature)

    # For demonstration, we'll just return True. Real verification would involve actual crypto operations.
    # You would typically use a library like 'cryptography' to perform the verification.
    # Example (conceptual, not runnable without full public key handling):
    # from cryptography.hazmat.primitives import hashes
    # from cryptography.hazmat.primitives.asymmetric import padding
    # from cryptography.hazmat.primitives.serialization import load_pem_public_key
    # public_key = load_pem_public_key(public_key_response.pem.encode('utf-8'))
    # try:
    #     public_key.verify(
    #         signature_bytes,
    #         request.message.encode('utf-8'),
    #         padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    #         hashes.SHA256()
    #     )
    #     return SignVerifyResponse(result=True)
    # except Exception:
    #     return SignVerifyResponse(result=False)

    # Dummy verification result
    is_verified = bool(signature_bytes) # A very basic check that a signature exists.

    return SignVerifyResponse(result=is_verified)
