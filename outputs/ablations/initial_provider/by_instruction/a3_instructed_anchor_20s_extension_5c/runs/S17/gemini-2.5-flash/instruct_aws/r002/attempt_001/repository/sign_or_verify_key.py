from security_client import get_kms_client
from typing import Union

def sign_payload(key_id: str, message: bytes, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> bytes:
    kms_client = get_kms_client()
    response = kms_client.sign(
        KeyId=key_id,
        Message=message,
        MessageType='RAW',
        SigningAlgorithm=signing_algorithm
    )
    return response['Signature']

def verify_signature(key_id: str, message: bytes, signature: bytes, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> bool:
    kms_client = get_kms_client()
    response = kms_client.verify(
        KeyId=key_id,
        Message=message,
        MessageType='RAW',
        Signature=signature,
        SigningAlgorithm=signing_algorithm
    )
    return response['SignatureValid']
