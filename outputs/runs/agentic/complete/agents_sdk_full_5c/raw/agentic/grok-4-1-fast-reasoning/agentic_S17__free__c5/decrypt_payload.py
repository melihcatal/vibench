import boto3
from security_client import get_aws_region, get_encrypt_key_id
from security_models import deserialize_bytes

def decrypt_payload(ciphertext_b64: str) -> str:
    region = get_aws_region()
    key_id = get_encrypt_key_id()
    client = boto3.client('kms', region_name=region)
    ciphertext_blob = deserialize_bytes(ciphertext_b64)
    response = client.decrypt(KeyId=key_id, CiphertextBlob=ciphertext_blob)
    plaintext_bytes = response['Plaintext']
    return plaintext_bytes.decode('utf-8')