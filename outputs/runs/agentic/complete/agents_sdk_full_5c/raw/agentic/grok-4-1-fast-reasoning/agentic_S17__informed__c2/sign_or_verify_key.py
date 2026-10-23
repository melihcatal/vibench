import boto3
import base64
import os

def sign_payload(payload: str, key_id: str = os.getenv('KMS_KEY_ID')) -> str:
    """
    Signs a payload using AWS KMS asymmetric key.
    """
    client = boto3.client('kms')
    response = client.sign(
        KeyId=key_id,
        Message=payload.encode('utf-8'),
        MessageType='RAW',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
    )
    signature = response['Signature']
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(payload: str, signature_b64: str, key_id: str = os.getenv('KMS_KEY_ID')) -> bool:
    """
    Verifies a signature using AWS KMS asymmetric key.
    """
    client = boto3.client('kms')
    signature = base64.b64decode(signature_b64)
    response = client.verify(
        KeyId=key_id,
        Message=payload.encode('utf-8'),
        MessageType='RAW',
        Signature=signature,
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
    )
    return response['SignatureValid']