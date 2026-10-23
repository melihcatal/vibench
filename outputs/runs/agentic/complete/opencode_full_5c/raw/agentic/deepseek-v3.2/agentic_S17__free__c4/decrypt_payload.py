import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import boto3
from botocore.exceptions import ClientError


def decrypt_payload(encryption_result):
    """
    Decrypt a ciphertext payload using AWS KMS managed key.

    Args:
        encryption_result: dict containing ciphertext, encrypted_key, and key_id

    Returns:
        Decrypted plaintext string
    """
    if not encryption_result or "ciphertext" not in encryption_result:
        raise ValueError("Invalid encryption result format")

    ciphertext = encryption_result["ciphertext"]
    encrypted_key = encryption_result.get("encrypted_key")
    key_id = encryption_result.get("key_id")

    if not encrypted_key:
        raise ValueError("Missing encrypted key in encryption result")

    # Decode base64 strings
    try:
        combined = base64.b64decode(ciphertext)
        encrypted_key_bytes = base64.b64decode(encrypted_key)
    except Exception as e:
        raise ValueError(f"Invalid base64 encoding: {e}")

    # Extract IV (16 bytes), tag (16 bytes), and actual ciphertext
    if len(combined) < 32:
        raise ValueError("Invalid ciphertext format")

    iv = combined[:16]
    tag = combined[16:32]
    actual_ciphertext = combined[32:]

    # Initialize AWS KMS client
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Decrypt the data key using KMS
    try:
        response = kms_client.decrypt(CiphertextBlob=encrypted_key_bytes)
    except ClientError as e:
        raise Exception(f"AWS KMS decryption error: {e}")

    plaintext_key = response["Plaintext"]

    # Decrypt the ciphertext using AES-GCM
    cipher = Cipher(
        algorithms.AES(plaintext_key), modes.GCM(iv, tag), backend=default_backend()
    )
    decryptor = cipher.decryptor()

    # Add associated data for authentication
    decryptor.authenticate_additional_data(b"encryption-context")

    try:
        plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

    return plaintext.decode("utf-8")
