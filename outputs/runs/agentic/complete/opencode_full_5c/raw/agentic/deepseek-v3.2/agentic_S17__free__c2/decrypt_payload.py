import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import boto3
from botocore.exceptions import ClientError


def decrypt_payload(encryption_data: dict) -> str:
    """
    Decrypt a ciphertext payload using AWS KMS managed key.

    Args:
        encryption_data: Dictionary containing:
            - ciphertext: base64 encoded ciphertext
            - encrypted_key: base64 encoded encrypted data key
            - iv: base64 encoded initialization vector
            - tag: base64 encoded authentication tag
            - key_id: AWS KMS key ID (optional)

    Returns:
        Decrypted plaintext string
    """
    # Initialize AWS KMS client
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        # Decode base64 fields
        ciphertext = base64.b64decode(encryption_data["ciphertext"])
        encrypted_key = base64.b64decode(encryption_data["encrypted_key"])
        iv = base64.b64decode(encryption_data["iv"])
        tag = base64.b64decode(encryption_data["tag"])

        # Get key_id from data or environment
        key_id = encryption_data.get("key_id") or os.environ.get(
            "AWS_KMS_KEY_ID", "alias/aws/encryption-key"
        )

        # Decrypt the data key using KMS
        decrypt_response = kms_client.decrypt(
            CiphertextBlob=encrypted_key, KeyId=key_id
        )

        plaintext_key = decrypt_response["Plaintext"]

        # Create cipher using AES-GCM
        cipher = Cipher(
            algorithms.AES(plaintext_key), modes.GCM(iv, tag), backend=default_backend()
        )

        decryptor = cipher.decryptor()

        # Decrypt the ciphertext
        plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()

        # Convert to string
        plaintext = plaintext_bytes.decode("utf-8")

        return plaintext

    except KeyError as e:
        raise Exception(f"Missing required field in encryption data: {str(e)}")
    except ClientError as e:
        raise Exception(f"AWS KMS decryption failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")
