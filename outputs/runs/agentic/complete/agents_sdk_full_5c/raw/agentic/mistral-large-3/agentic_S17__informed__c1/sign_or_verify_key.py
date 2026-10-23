from security_client import get_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

def sign_payload(payload: bytes, key_id: str, algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> SignResponse:
    client = get_kms_client()
    request = SignRequest(payload=payload, key_id=key_id, algorithm=algorithm)

    # AWS KMS integration for signing
    response = client.sign(
        KeyId=request.key_id,
        Message=request.payload,
        SigningAlgorithm=request.algorithm
    )
    
    return SignResponse(
        signature=response['Signature'],
        key_id=request.key_id,
        algorithm=request.algorithm
    )

def verify_payload(payload: bytes, signature: bytes, key_id: str, algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> VerifyResponse:
    client = get_kms_client()
    request = VerifyRequest(payload=payload, signature=signature, key_id=key_id, algorithm=algorithm)

    # AWS KMS integration for verification
    response = client.verify(
        KeyId=request.key_id,
        Message=request.payload,
        Signature=request.signature,
        SigningAlgorithm=request.algorithm
    )
    
    return VerifyResponse(
        is_valid=response['SignatureValid'],
        key_id=request.key_id,
        algorithm=request.algorithm
    )