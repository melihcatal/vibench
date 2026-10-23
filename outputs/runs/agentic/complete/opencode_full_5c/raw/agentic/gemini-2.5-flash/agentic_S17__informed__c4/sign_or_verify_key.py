import os
from security_client import KMSClient
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_data_with_kms(key_id: str, digest: bytes) -> SignResponse:
    kms_client = KMSClient()
    request = SignRequest(key_id=key_id, digest=digest)
    response = kms_client.sign_digest(request)
    return response


def verify_signature_with_kms(
    key_id: str, digest: bytes, signature: bytes
) -> VerifyResponse:
    kms_client = KMSClient()
    request = VerifyRequest(key_id=key_id, digest=digest, signature=signature)
    response = kms_client.verify_digest(request)
    return response
