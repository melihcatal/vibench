from security_client import get_kms_client
import base64

def sign_message(message: str, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256', region: str = None) -> str:
    client = get_kms_client(region)
    response = client.sign(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        SigningAlgorithm=signing_algorithm
    )
    return base64.b64encode(response['Signature']).decode('utf-8')

def verify_signature(message: str, signature_b64: str, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256', region: str = None) -> bool:
    client = get_kms_client(region)
    signature = base64.b64decode(signature_b64)
    response = client.verify(
        KeyId=key_id,
        Message=message.encode('utf-8'),
        MessageType='RAW',
        Signature=signature,
        SigningAlgorithm=signing_algorithm
    )
    return response['SignatureValid']