from security_client import get_kms_client
from botocore.exceptions import ClientError

def sign_message(message: bytes, key_id: str, signing_algorithm: str = 'HMAC_SHA256') -> bytes:
    kms = get_kms_client()
    response = kms.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm=signing_algorithm,
        MessageType='RAW'
    )
    return response['Signature']

def verify_signature(message: bytes, signature: bytes, key_id: str, signing_algorithm: str = 'HMAC_SHA256') -> bool:
    kms = get_kms_client()
    try:
        kms.verify(
            KeyId=key_id,
            Message=message,
            MessageType='RAW',
            Signature=signature,
            SigningAlgorithm=signing_algorithm
        )
        return True
    except ClientError:
        return False