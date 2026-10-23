import boto3
import os
from typing import Tuple

def sign_message(message: bytes, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> bytes:
    """
    Signs a message using AWS KMS asymmetric key.
    """
    client = boto3.client('kms', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    response = client.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm=signing_algorithm,
        MessageType='RAW'
    )
    return response['Signature']

def verify_signature(message: bytes, signature: bytes, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> bool:
    """
    Verifies a signature using AWS KMS asymmetric key.
    """
    client = boto3.client('kms', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    try:
        response = client.verify(
            KeyId=key_id,
            Message=message,
            Signature=signature,
            SigningAlgorithm=signing_algorithm,
            MessageType='RAW'
        )
        return response['SignatureValid']
    except client.exceptions.InvalidSignatureException:
        return False
