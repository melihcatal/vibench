import boto3
from typing import Union
from security_client import get_aws_region, get_encrypt_key_id
from security_models import normalize_plaintext, serialize_bytes

def encrypt_payload(plaintext: Union[str, bytes]) -> str:
    region = get_aws_region()
    key_id = get_encrypt_key_id()
    client = boto3.client('kms', region_name=region)
    plaintext_bytes = normalize_plaintext(plaintext)
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext_bytes)
    ciphertext_blob = response['CiphertextBlob']
    return serialize_bytes(ciphertext_blob)