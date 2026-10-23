import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import boto3
from botocore.exceptions import ClientError


def encrypt_payload(plaintext: str, key_id: str = None) -> dict:
    """
    Encrypt a plaintext payload using AWS KMS managed key.

    Args:
        plaintext: The text to encrypt
        key_id: AWS KMS key ID or alias (defaults to env var)

    Returns:
        Dictionary with ciphertext and metadata
    """
    if key_id is None:
        key_id = os.getenv("AWS_KMS_KEY_ID", "alias/encryption-key")

    kms_client = boto3.client("kms", region_name=os.getenv("AWS_REGION", "us-east-1"))

    try:
        response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext.encode("utf-8"),
            EncryptionAlgorithm="SYMMETRIC_DEFAULT",
        )

        ciphertext = base64.b64encode(response["CiphertextBlob"]).decode("utf-8")

        return {
            "ciphertext": ciphertext,
            "key_id": key_id,
            "encryption_algorithm": "SYMMETRIC_DEFAULT",
            "provider": "aws_kms",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS encryption failed: {e}")


if __name__ == "__main__":
    test_text = "Sensitive data to encrypt"
    result = encrypt_payload(test_text)
    print(f"Encryption result: {json.dumps(result, indent=2)}")
