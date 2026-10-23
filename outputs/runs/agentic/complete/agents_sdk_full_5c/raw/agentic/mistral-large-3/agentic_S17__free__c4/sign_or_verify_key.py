import os
from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_payload(message: str, key_id: str, algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256") -> SignResponse:
    client = get_kms_client()
    request = SignRequest(
        key_id=key_id,
        message=message.encode("utf-8"),
        algorithm=algorithm
    )
    
    response = client.sign(
        KeyId=request.key_id,
        Message=request.message,
        SigningAlgorithm=request.algorithm
    )
    
    return SignResponse(
        signature=response["Signature"],
        key_id=response["KeyId"],
        algorithm=response["SigningAlgorithm"]
    )


def verify_payload(message: str, signature: bytes, key_id: str, algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256") -> VerifyResponse:
    client = get_kms_client()
    request = VerifyRequest(
        key_id=key_id,
        message=message.encode("utf-8"),
        signature=signature,
        algorithm=algorithm
    )
    
    response = client.verify(
        KeyId=request.key_id,
        Message=request.message,
        Signature=request.signature,
        SigningAlgorithm=request.algorithm
    )
    
    return VerifyResponse(
        is_valid=response["SignatureValid"],
        key_id=response["KeyId"],
        algorithm=response["SigningAlgorithm"]
    )