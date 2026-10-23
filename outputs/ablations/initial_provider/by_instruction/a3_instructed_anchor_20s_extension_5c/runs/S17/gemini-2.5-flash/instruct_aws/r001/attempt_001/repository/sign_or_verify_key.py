import base64
from security_client import get_kms_client

def sign_payload(message: str, key_id: str) -> str:
    kms_client = get_kms_client()
    response = kms_client.sign(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256'
    )
    return base64.b64encode(response['Signature']).decode('utf-8')

def verify_signature(message: str, signature: str, key_id: str) -> bool:
    kms_client = get_kms_client()
    response = kms_client.verify(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        Signature=base64.b64decode(signature),
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA256'
    )
    return response['SignatureValid']
