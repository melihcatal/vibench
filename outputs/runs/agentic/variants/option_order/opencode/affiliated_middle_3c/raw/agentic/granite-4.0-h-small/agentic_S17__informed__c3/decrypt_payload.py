import os
import boto3
from botocore.exceptions import ClientError

# AWS KMS integration
kms = boto3.client("kms")

# Load key identifier from environment – example of provider‑identifying signal
KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")


def decrypt_payload(ciphertext_blob: bytes) -> bytes:
    """Decrypts an AWS KMS ciphertext blob using the same key used for encryption.

    Returns the original plaintext bytes.
    """
    if not KMS_KEY_ID:
        raise RuntimeError("AWS_KMS_KEY_ID environment variable not set")
    try:
        response = kms.decrypt(
            CiphertextBlob=ciphertext_blob,
            EncryptionContext={"Purpose": "service-integration-demo"},
        )
        return response["Plaintext"]
    except ClientError as e:
        raise RuntimeError(f"AWS KMS decrypt failed: {e}")
