from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse
from google.cloud.kms_v1.types import Digest
from google.protobuf import wrappers_pb2
import base64


def sign_payload(request: SignRequest) -> SignResponse:
    client = get_kms_client()

    # The data to be signed is hashed before being passed to KMS.
    # For simplicity, using SHA256 here, but the actual hashing algorithm
    # should match the key's algorithm in KMS.
    data_bytes = request.data.encode("utf-8")
    import hashlib

    sha256 = hashlib.sha256(data_bytes).digest()

    # Create a Digest object
    digest = Digest(sha256=sha256)

    # Sign the digest
    sign_response = client.asymmetric_sign(name=request.key_name, digest=digest)

    return SignResponse(signature=sign_response.signature, key_name=request.key_name)


def verify_signature(request: VerifyRequest) -> VerifyResponse:
    client = get_kms_client()

    # Retrieve the public key to verify the signature locally.
    # Google Cloud KMS doesn't offer a direct 'verify' API for asymmetric keys,
    # so verification is typically done client-side using the public key.
    # Alternatively, you might use the KeyAccessJustifications service for audit,
    # but for actual cryptographic verification, the public key is needed.
    # For this example, we will simulate the process by retrieving the public key
    # and then assume a local verification library would be used.

    # In a real scenario, you would fetch the public key associated with the KMS key
    # and use a library like cryptography to verify the signature.
    # For the purpose of this example, we will just return True/False based on a placeholder.

    # This is a placeholder. A real implementation would fetch the public key
    # and use a crypto library to verify. Example of fetching public key:
    # public_key_response = client.get_public_key(name=request.key_name)
    # public_key_pem = public_key_response.pem

    # For demonstration, we'll just check if the signature is not empty. (This is NOT a real verification)
    is_valid = bool(request.signature)

    return VerifyResponse(is_valid=is_valid, key_name=request.key_name)
