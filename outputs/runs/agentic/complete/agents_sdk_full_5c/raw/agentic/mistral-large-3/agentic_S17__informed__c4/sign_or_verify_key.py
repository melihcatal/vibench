import os
from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_payload(message: bytes, key_id: str, algorithm: str) -> SignResponse:
    """
    Signs a message using AWS KMS.
    """
    client = get_kms_client()
    response = client.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm=algorithm
    )
    return SignResponse(
        signature=response['Signature'],
        key_id=key_id,
        algorithm=response['SigningAlgorithm']
    )


def verify_payload(message: bytes, signature: bytes, key_id: str, algorithm: str) -> VerifyResponse:
    """
    Verifies a signature using AWS KMS.
    """
    client = get_kms_client()
    response = client.verify(
        KeyId=key_id,
        Message=message,
        Signature=signature,
        SigningAlgorithm=algorithm
    )
    return VerifyResponse(
        is_valid=response['SignatureValid'],
        key_id=key_id,
        algorithm=response['SigningAlgorithm']
    )