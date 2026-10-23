import boto3
import os

def decrypt_payload(ciphertext_blob: bytes) -> bytes:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    kms_client = boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob,
    )
    return response["Plaintext"]

