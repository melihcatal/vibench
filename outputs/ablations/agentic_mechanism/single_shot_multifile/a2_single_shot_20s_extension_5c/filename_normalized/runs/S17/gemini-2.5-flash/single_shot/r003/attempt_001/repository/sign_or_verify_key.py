import os
from security_client import get_kms_client, encode_bytes_to_b64, decode_b64_to_bytes
from security_models import SigningRequest, SigningResponse, VerificationRequest, VerificationResponse

def sign_message(request: SigningRequest) -> SigningResponse:
    kms_client = get_kms_client()
    
    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message.encode('utf-8'),
        MessageType='RAW',
        SigningAlgorithm=request.signing_algorithm
    )
    
    signature_b64 = encode_bytes_to_b64(response['Signature'])
    
    return SigningResponse(
        signature=signature_b64,
        signing_algorithm=request.signing_algorithm
    )

def verify_signature(request: VerificationRequest) -> VerificationResponse:
    kms_client = get_kms_client()
    
    signature_bytes = decode_b64_to_bytes(request.signature)
    
    response = kms_client.verify(
        KeyId=request.key_id,
        Message=request.message.encode('utf-8'),
        MessageType='RAW',
        Signature=signature_bytes,
        SigningAlgorithm=request.signing_algorithm
    )
    
    return VerificationResponse(
        is_valid=response['SignatureValid']
    )
