from security_client import get_kms_client
from security_models import to_bytes, b64encode, b64decode

def sign_message(message: str, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> str:
    client = get_kms_client()
    message_bytes = to_bytes(message)
    response = client.sign(
        KeyId=key_id,
        Message=message_bytes,
        MessageType='RAW',
        SigningAlgorithm=signing_algorithm
    )
    return b64encode(response['Signature'])

def verify_signature(message: str, signature_b64: str, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> bool:
    client = get_kms_client()
    message_bytes = to_bytes(message)
    signature_bytes = b64decode(signature_b64)
    try:
        client.verify(
            KeyId=key_id,
            Message=message_bytes,
            MessageType='RAW',
            Signature=signature_bytes,
            SigningAlgorithm=signing_algorithm
        )
        return True
    except client.exceptions.InvalidSignatureException:
        return False