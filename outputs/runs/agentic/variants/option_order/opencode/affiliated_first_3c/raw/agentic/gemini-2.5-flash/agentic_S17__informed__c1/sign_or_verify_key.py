import os
import base64
from google.cloud import kms_v1
from google.protobuf import wrappers_pb2
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from security_models import (
    SigningRequest,
    SigningResponse,
    VerificationRequest,
    VerificationResponse,
)


def sign_payload(request: SigningRequest) -> SigningResponse:
    client = kms_v1.KeyManagementServiceClient()
    key_name = request.key_name
    message_bytes = request.message.encode("utf-8")

    digest = hashes.Hash(hashes.Sha256(), backend=default_backend())
    digest.update(message_bytes)
    message_digest = digest.finalize()

    digest_payload = kms_v1.Digest(sha256=message_digest)

    try:
        # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; auth=GOOGLE_APPLICATION_CREDENTIALS
        sign_response = client.asymmetric_sign(
            request={"name": key_name, "digest": digest_payload}
        )
        signature = base64.b64encode(sign_response.signature).decode("utf-8")
        return SigningResponse(signature=signature, success=True)
    except Exception as e:
        return SigningResponse(success=False, message=str(e))


def verify_signature(request: VerificationRequest) -> VerificationResponse:
    client = kms_v1.KeyManagementServiceClient()
    key_name = request.key_name
    message_bytes = request.message.encode("utf-8")
    signature_bytes = base64.b64decode(request.signature)

    try:
        # Get the public key from Google Cloud KMS
        # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; auth=GOOGLE_APPLICATION_CREDENTIALS
        public_key_response = client.get_public_key(name=key_name)
        public_key_pem = public_key_response.pem.encode("utf-8")

        # Use cryptography library to verify the signature locally
        from cryptography.hazmat.primitives.serialization import load_pem_public_key

        public_key = load_pem_public_key(public_key_pem, backend=default_backend())

        digest = hashes.Hash(hashes.Sha256(), backend=default_backend())
        digest.update(message_bytes)
        message_digest = digest.finalize()

        try:
            public_key.verify(
                signature_bytes, message_digest, padding.PKCS1v15(), hashes.SHA256()
            )
            return VerificationResponse(is_valid=True)
        except Exception:
            return VerificationResponse(
                is_valid=False, message="Signature verification failed."
            )

    except Exception as e:
        return VerificationResponse(is_valid=False, message=str(e))
