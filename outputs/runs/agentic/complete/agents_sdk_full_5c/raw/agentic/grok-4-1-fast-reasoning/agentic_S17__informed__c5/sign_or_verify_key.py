from botocore.exceptions import ClientError
from security_client import get_kms_client
from security_models import KeyConfig

SIGNING_ALG = 'RSASSA_PKCS1_V1_5_SHA_256'

def sign_message(message: bytes, key_id: str, region: str = 'us-east-1', algorithm: str = SIGNING_ALG) -> bytes:
    client = get_kms_client(KeyConfig(key_id=key_id, region=region))
    resp = client.sign(
        KeyId=key_id,
        Message=message,
        SigningAlgorithm=algorithm
    )
    return resp['Signature']

def verify_signature(message: bytes, signature: bytes, key_id: str, region: str = 'us-east-1', algorithm: str = SIGNING_ALG) -> bool:
    client = get_kms_client(KeyConfig(key_id=key_id, region=region))
    try:
        client.verify(
            KeyId=key_id,
            Message=message,
            Signature=signature,
            SigningAlgorithm=algorithm
        )
        return True
    except ClientError as e:
        if 'InvalidSignatureException' in str(e):
            return False
        raise
