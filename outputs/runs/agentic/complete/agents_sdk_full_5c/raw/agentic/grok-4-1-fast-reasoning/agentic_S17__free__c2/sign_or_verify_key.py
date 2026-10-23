from security_client import get_kms_client
from security_models import to_bytes, serialize_blob, deserialize_blob

def sign_message(message: str, key_id: str) -> str:
    client = get_kms_client()
    response = client.sign(
        KeyId=key_id,
        Message=to_bytes(message),
        SigningAlgorithm='RSASSA_PKCS1_V1_1_SHA_256',
        MessageType='RAW'
    )
    return serialize_blob(response['Signature'])

def verify_signature(message: str, signature: str, key_id: str) -> bool:
    client = get_kms_client()
    response = client.verify(
        KeyId=key_id,
        Message=to_bytes(message),
        Signature=deserialize_blob(signature),
        SigningAlgorithm='RSASSA_PKCS1_V1_1_SHA_256',
        MessageType='RAW'
    )
    return response['SignatureValid']