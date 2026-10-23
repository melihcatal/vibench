import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import boto3
from botocore.exceptions import ClientError


def encrypt_payload(plaintext, key_id=None, context=None):
    """
    Encrypt plaintext using AWS KMS managed key.

    Args:
        plaintext: String or bytes to encrypt
        key_id: AWS KMS key ID or alias (defaults to environment variable)
        context: Optional encryption context dict

    Returns:
        dict with ciphertext and metadata
    """
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    if key_id is None:
        key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/encryption-key")

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = kms_client.encrypt(
            KeyId=key_id, Plaintext=plaintext, EncryptionContext=context or {}
        )

        ciphertext_blob = response["CiphertextBlob"]

        return {
            "ciphertext": base64.b64encode(ciphertext_blob).decode("utf-8"),
            "key_id": key_id,
            "encryption_context": context or {},
            "provider": "aws_kms",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS encryption failed: {e}")


if __name__ == "__main__":
    test_text = "Sensitive data to encrypt"
    result = encrypt_payload(test_text)
    print(f"Encryption result: {json.dumps(result, indent=2)}")
