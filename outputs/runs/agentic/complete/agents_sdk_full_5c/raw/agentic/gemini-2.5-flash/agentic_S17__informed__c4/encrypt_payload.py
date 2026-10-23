import boto3
import os

def encrypt_payload(key_id: str, plaintext: bytes) -> bytes:
    """
    Encrypts a plaintext payload using AWS KMS.
    """
    kms_client = boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext,
    )
    return response["CiphertextBlob"]

