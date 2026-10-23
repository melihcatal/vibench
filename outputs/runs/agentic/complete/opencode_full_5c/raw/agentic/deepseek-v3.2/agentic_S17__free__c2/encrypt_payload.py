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
        plaintext: The plaintext to encrypt
        key_id: Optional AWS KMS key ID. If not provided, uses default key.

    Returns:
        Dictionary with ciphertext and encryption metadata
    """
    # Initialize AWS KMS client
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Use default key if not specified
    if not key_id:
        key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/aws/encryption-key")

    try:
        # Generate a data key from KMS
        data_key_response = kms_client.generate_data_key(
            KeyId=key_id, KeySpec="AES_256"
        )

        plaintext_key = data_key_response["Plaintext"]
        encrypted_key = data_key_response["CiphertextBlob"]

        # Generate a random IV
        iv = os.urandom(16)

        # Create cipher using AES-GCM
        cipher = Cipher(
            algorithms.AES(plaintext_key), modes.GCM(iv), backend=default_backend()
        )

        encryptor = cipher.encryptor()

        # Encrypt the plaintext
        ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()

        # Get the authentication tag
        tag = encryptor.tag

        # Prepare response
        result = {
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
            "encrypted_key": base64.b64encode(encrypted_key).decode("utf-8"),
            "iv": base64.b64encode(iv).decode("utf-8"),
            "tag": base64.b64encode(tag).decode("utf-8"),
            "key_id": key_id,
            "algorithm": "AES-GCM",
            "key_size": 256,
            "provider": "aws_kms",
        }

        return result

    except ClientError as e:
        raise Exception(f"AWS KMS encryption failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Encryption failed: {str(e)}")
