import boto3
import os


def encrypt_payload(plaintext: bytes, key_id: str = None) -> bytes:
    if key_id is None:
        key_id = os.getenv("AWS_KMS_KEY_ID")
    kms = boto3.client("kms", region_name="us-east-1")
    response = kms.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response["CiphertextBlob"]
