import boto3
from security_client import get_aws_region, get_sign_key_id
from security_models import serialize_bytes, deserialize_bytes, normalize_plaintext

def sign_message(message: str) -> str:
    region = get_aws_region()
    key_id = get_sign_key_id()
    client = boto3.client('kms', region_name=region)
    msg_bytes = normalize_plaintext(message)
    response = client.sign(
        KeyId=key_id,
        Message=msg_bytes,
        MessageType='RAW',
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
    )
    return serialize_bytes(response['Signature'])

def verify_message(message: str, signature_b64: str) -> bool:
    region = get_aws_region()
    key_id = get_sign_key_id()
    client = boto3.client('kms', region_name=region)
    msg_bytes = normalize_plaintext(message)
    sig_bytes = deserialize_bytes(signature_b64)
    response = client.verify(
        KeyId=key_id,
        Message=msg_bytes,
        MessageType='RAW',
        Signature=sig_bytes,
        SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
    )
    return response['SignatureValid']