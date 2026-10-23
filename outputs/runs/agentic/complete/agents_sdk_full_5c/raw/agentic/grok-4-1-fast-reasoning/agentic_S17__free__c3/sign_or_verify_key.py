from security_client import kms_client, ASYMMETRIC_KEY_ID
from security_models import b64encode, b64decode, normalize_payload

def sign_message(message: str) -> str:
    msg_bytes = normalize_payload(message)
    response = kms_client.sign(
        KeyId=ASYMMETRIC_KEY_ID,
        Message=msg_bytes,
        MessageType='RAW',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
    )
    return b64encode(response['Signature'])

def verify_signature(message: str, signature_b64: str) -> bool:
    msg_bytes = normalize_payload(message)
    signature = b64decode(signature_b64)
    response = kms_client.verify(
        KeyId=ASYMMETRIC_KEY_ID,
        Message=msg_bytes,
        MessageType='RAW',
        Signature=signature,
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
    )
    return response['SignatureValid']
