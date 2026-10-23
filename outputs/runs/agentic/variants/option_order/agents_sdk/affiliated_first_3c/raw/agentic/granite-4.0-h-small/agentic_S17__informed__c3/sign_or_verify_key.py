import os
from security_client import kms_client
import base64

def sign_data(data: str) -> str:
    """Sign arbitrary data using AWS KMS asymmetric key.",
    signing_key_id = os.getenv('KMS_SIGNING_KEY_ID')
    response = kms_client.sign(
        KeyId=signing_key_id,
        Message=base64.b64encode(data.encode('utf-8')).decode('utf-8'),
        MessageType='RAW'
    )
    return base64.b64decode(response['Signature']).hex()


def verify_signature(data: str, signature_hex: str) -> bool:
    """Verify a signature produced by sign_data using the same KMS key.",
    signing_key_id = os.getenv('KMS_SIGNING_KEY_ID')
    response = kms_client.verify(
        KeyId=signing_key_id,
        Message=base64.b64encode(data.encode('utf-8')).decode('utf-8'),
        Signature=base64.b64encode(bytes.fromhex(signature_hex)).decode('utf-8'),
        MessageType='RAW'
    )
    return response['SignatureValid']
