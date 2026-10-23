import os
import json
import base64
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import boto3
from botocore.exceptions import ClientError


def envelope_encrypt(plaintext: str, key_id: str = None) -> dict:
    """
    Implement envelope encryption using AWS KMS.

    Steps:
    1. Generate a data encryption key (DEK) locally
    2. Encrypt the plaintext with the DEK using AES-256-GCM
    3. Encrypt the DEK with AWS KMS (enveloping)

    Args:
        plaintext: The text to encrypt
        key_id: AWS KMS key ID or alias

    Returns:
        Dictionary with encrypted data, encrypted DEK, and metadata
    """
    if key_id is None:
        key_id = os.getenv("AWS_KMS_KEY_ID", "alias/envelope-key")

    kms_client = boto3.client("kms", region_name=os.getenv("AWS_REGION", "us-east-1"))

    # Step 1: Generate data encryption key (DEK)
    dek = secrets.token_bytes(32)  # 256-bit key for AES-256
    iv = secrets.token_bytes(12)  # 96-bit IV for GCM

    # Step 2: Encrypt plaintext with DEK using AES-256-GCM
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
    tag = encryptor.tag

    # Step 3: Encrypt DEK with AWS KMS
    try:
        kms_response = kms_client.encrypt(
            KeyId=key_id, Plaintext=dek, EncryptionAlgorithm="SYMMETRIC_DEFAULT"
        )
        encrypted_dek = base64.b64encode(kms_response["CiphertextBlob"]).decode("utf-8")
    except ClientError as e:
        raise Exception(f"AWS KMS DEK encryption failed: {e}")

    return {
        "encrypted_data": base64.b64encode(ciphertext).decode("utf-8"),
        "encrypted_dek": encrypted_dek,
        "iv": base64.b64encode(iv).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8"),
        "key_id": key_id,
        "encryption_mode": "AES-256-GCM",
        "provider": "aws_kms",
    }


def envelope_decrypt(
    encrypted_data: str, encrypted_dek: str, iv: str, tag: str, key_id: str = None
) -> str:
    """
    Decrypt envelope-encrypted data.

    Args:
        encrypted_data: Base64-encoded encrypted data
        encrypted_dek: Base64-encoded encrypted DEK
        iv: Base64-encoded initialization vector
        tag: Base64-encoded authentication tag
        key_id: AWS KMS key ID or alias

    Returns:
        Decrypted plaintext
    """
    kms_client = boto3.client("kms", region_name=os.getenv("AWS_REGION", "us-east-1"))

    # Step 1: Decrypt DEK with AWS KMS
    try:
        dek_response = kms_client.decrypt(
            CiphertextBlob=base64.b64decode(encrypted_dek),
            KeyId=key_id if key_id else None,
            EncryptionAlgorithm="SYMMETRIC_DEFAULT",
        )
        dek = dek_response["Plaintext"]
    except ClientError as e:
        raise Exception(f"AWS KMS DEK decryption failed: {e}")

    # Step 2: Decrypt data with DEK
    ciphertext = base64.b64decode(encrypted_data)
    iv_bytes = base64.b64decode(iv)
    tag_bytes = base64.b64decode(tag)

    cipher = Cipher(
        algorithms.AES(dek), modes.GCM(iv_bytes, tag_bytes), backend=default_backend()
    )
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode("utf-8")


if __name__ == "__main__":
    test_text = "Highly sensitive data for envelope encryption"
    encrypted = envelope_encrypt(test_text)
    print(f"Envelope encrypted: {json.dumps(encrypted, indent=2)}")

    decrypted = envelope_decrypt(
        encrypted["encrypted_data"],
        encrypted["encrypted_dek"],
        encrypted["iv"],
        encrypted["tag"],
    )
    print(f"Decrypted: {decrypted}")
