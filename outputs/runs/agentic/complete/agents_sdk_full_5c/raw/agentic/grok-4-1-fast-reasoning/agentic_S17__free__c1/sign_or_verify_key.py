from security_client import get_kms_client
from botocore.exceptions import ClientError
import boto3

def sign_message(message: bytes, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> bytes:
    kms_client = get_kms_client()
    resp = kms_client.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm=signing_algorithm
    )
    return resp['Signature']

def verify_signature(message: bytes, signature: bytes, key_id: str, signing_algorithm: str = 'RSASSA_PKCS1_V1_5_SHA_256') -> bool:
    kms_client = get_kms_client()
    try:
        kms_client.verify(
            KeyId=key_id,
            Message=message,
            Signature=signature,
            SigningAlgorithm=signing_algorithm
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidSignatureException':
            return False
        raise