import boto3
import os


def decrypt_payload(ciphertext: bytes, key_id: str = None) -> bytes:
    if key_id is None:
        key_id = os.getenv("AWS_KMS_KEY_ID")
    kms = boto3.client("kms", region_name="us-east-1")
    response = kms.decrypt(CiphertextBlob=ciphertext)
    return response["Plaintext"]
