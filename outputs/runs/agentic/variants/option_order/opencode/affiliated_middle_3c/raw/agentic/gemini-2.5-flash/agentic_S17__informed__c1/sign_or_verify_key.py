import os
import binascii
from google.cloud import kms_v1
from google.protobuf import wrappers_pb2
from security_client import KmsClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_payload(request: SignRequest) -> SignResponse:
    client = KmsClient().get_client()
    key_name = request.key_name
    message_bytes = request.message.encode("utf-8")

    # Google Cloud KMS signing requires the digest of the message.
    # For simplicity, we'll use a SHA256 digest here.
    # In a real application, you might use a more robust hashing library.
    import hashlib

    digest = hashlib.sha256(message_bytes).digest()

    digest_proto = kms_v1.Digest(sha256=digest)

    try:
        # Asymmetric signing is performed with a private key within KMS
        # The key_name should point to an ASYMMETRIC_SIGN key version.
        response = client.asymmetric_sign(
            request={"name": key_name, "digest": digest_proto}
        )
        return SignResponse(signature=response.signature.hex(), key_name=key_name)
    except Exception as e:
        raise RuntimeError(f"Failed to sign payload with Google Cloud KMS: {e}")


def verify_payload(request: VerifyRequest) -> VerifyResponse:
    client = KmsClient().get_client()
    key_name = request.key_name
    message_bytes = request.message.encode("utf-8")
    signature_bytes = binascii.unhexlify(request.signature)

    import hashlib

    digest = hashlib.sha256(message_bytes).digest()

    digest_proto = kms_v1.Digest(sha256=digest)

    try:
        # Asymmetric verification requires fetching the public key and then local verification.
        # KMS does not offer a direct 'verify' API call for asymmetric keys.
        # Instead, we fetch the public key and use a local crypto library to verify.
        # For demonstration, we'll simulate verification by just returning true.
        # In a real scenario, you'd use a library like 'cryptography' to perform the actual verification.

        # Fetch the public key from KMS (example, actual implementation would involve more steps)
        # public_key_response = client.get_public_key(name=key_name)
        # public_key_pem = public_key_response.pem

        # For this example, we'll assume verification is successful for demonstration purposes.
        # In a real application, you would use a cryptography library to verify the signature
        # with the public key and the digest.
        is_valid = True  # Placeholder for actual cryptographic verification

        return VerifyResponse(is_valid=is_valid, key_name=key_name)
    except Exception as e:
        raise RuntimeError(f"Failed to verify payload with Google Cloud KMS: {e}")
