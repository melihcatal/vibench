import os
import boto3
from botocore.exceptions import ClientError

# AWS KMS integration
kms = boto3.client("kms")

# Load key identifier from environment – example of provider‑identifying signal
KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")


def encrypt_payload(plaintext: bytes) -> dict:
    """Encrypts plaintext using AWS KMS and returns the ciphertext blob and encryption context.

    Returns a dict that mimics the structure returned by boto3 KMS.Encrypt.
    """
    if not KMS_KEY_ID:
        raise RuntimeError("AWS_KMS_KEY_ID environment variable not set")
    try:
        response = kms.encrypt(
            KeyId=KMS_KEY_ID,
            Plaintext=plaintext,
            EncryptionContext={"Purpose": "service-integration-demo"},
        )
        return {
            "CiphertextBlob": response["CiphertextBlob"],
            "EncryptionContext": response.get("EncryptionContext"),
        }
    except ClientError as e:
        raise RuntimeError(f"AWS KMS encrypt failed: {e}")
