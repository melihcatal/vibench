import boto3
from security_client import get_kms_client

def sign_or_verify_key(message, signature):
    kms_client = get_kms_client()
    response = kms_client.verify(
        KeyId='alias/example_key',
        Message=message,
        Signature=signature,
        MessageType='RAW',
        SigningAlgorithm='RSASSA_PSS_SHA_256'
    )
    return response['SignatureValid']