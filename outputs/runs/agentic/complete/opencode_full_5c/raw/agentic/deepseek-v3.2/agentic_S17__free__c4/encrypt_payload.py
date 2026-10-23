import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import boto3
from botocore.exceptions import ClientError


def encrypt_payload(plaintext, key_id=None):
    """
    Encrypt a plaintext payload using AWS KMS managed key.

    Args:
        plaintext: The plaintext string to encrypt
        key_id: Optional AWS KMS key ID or alias (defaults to env var)

    Returns:
        dict with ciphertext and encryption context
    """
    if not plaintext:
        raise ValueError("Plaintext cannot be empty")

    # Use environment variable or provided key ID
    if not key_id:
        key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/encryption-key")

    # Initialize AWS KMS client
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Generate a data key from KMS
    try:
        response = kms_client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    except ClientError as e:
        raise Exception(f"AWS KMS error: {e}")

    plaintext_key = response["Plaintext"]
    encrypted_key = response["CiphertextBlob"]

    # Generate a random IV
    iv = os.urandom(16)

    # Encrypt the plaintext using AES-GCM
    cipher = Cipher(
        algorithms.AES(plaintext_key), modes.GCM(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()

    # Add associated data for authentication
    encryptor.authenticate_additional_data(b"encryption-context")

    ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
    tag = encryptor.tag

    # Combine IV, ciphertext, and tag
    combined = iv + tag + ciphertext

    # Base64 encode for safe storage/transmission
    encoded_ciphertext = base64.b64encode(combined).decode("utf-8")
    encoded_encrypted_key = base64.b64encode(encrypted_key).decode("utf-8")

    return {
        "ciphertext": encoded_ciphertext,
        "encrypted_key": encoded_encrypted_key,
        "key_id": key_id,
        "algorithm": "AES-GCM-256",
        "provider": "aws_kms",
    }
