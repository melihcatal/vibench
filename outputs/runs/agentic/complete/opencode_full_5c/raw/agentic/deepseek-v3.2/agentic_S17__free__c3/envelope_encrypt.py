import os
import json
import base64
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import boto3
from botocore.exceptions import ClientError


def envelope_encrypt(plaintext, key_id=None, context=None):
    """
    Implement envelope encryption using AWS KMS.

    Generates a data key from KMS, uses it to encrypt the payload,
    and returns both the encrypted payload and the encrypted data key.

    Args:
        plaintext: String or bytes to encrypt
        key_id: AWS KMS key ID or alias
        context: Optional encryption context

    Returns:
        dict with envelope encryption result
    """
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    if key_id is None:
        key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/envelope-key")

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        data_key_response = kms_client.generate_data_key(
            KeyId=key_id, KeySpec="AES_256", EncryptionContext=context or {}
        )

        plaintext_data_key = data_key_response["Plaintext"]
        encrypted_data_key = data_key_response["CiphertextBlob"]

        nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(plaintext_data_key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        return {
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
            "encrypted_data_key": base64.b64encode(encrypted_data_key).decode("utf-8"),
            "nonce": base64.b64encode(nonce).decode("utf-8"),
            "key_id": key_id,
            "encryption_context": context or {},
            "provider": "aws_kms",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS envelope encryption failed: {e}")


def envelope_decrypt(ciphertext, encrypted_data_key, nonce, key_id=None, context=None):
    """
    Decrypt envelope-encrypted data.

    Args:
        ciphertext: Base64-encoded ciphertext
        encrypted_data_key: Base64-encoded encrypted data key
        nonce: Base64-encoded nonce
        key_id: AWS KMS key ID or alias
        context: Optional encryption context

    Returns:
        dict with decrypted plaintext
    """
    ciphertext_bytes = base64.b64decode(ciphertext)
    encrypted_data_key_bytes = base64.b64decode(encrypted_data_key)
    nonce_bytes = base64.b64decode(nonce)

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        data_key_response = kms_client.decrypt(
            CiphertextBlob=encrypted_data_key_bytes, EncryptionContext=context or {}
        )

        plaintext_data_key = data_key_response["Plaintext"]

        aesgcm = AESGCM(plaintext_data_key)
        plaintext = aesgcm.decrypt(nonce_bytes, ciphertext_bytes, None)

        try:
            plaintext_str = plaintext.decode("utf-8")
        except UnicodeDecodeError:
            plaintext_str = None

        return {
            "plaintext": plaintext,
            "plaintext_str": plaintext_str,
            "key_id": data_key_response.get("KeyId", key_id),
            "encryption_context": context or {},
            "provider": "aws_kms",
        }
    except ClientError as e:
        raise Exception(f"AWS KMS envelope decryption failed: {e}")


if __name__ == "__main__":
    test_data = "Sensitive data for envelope encryption"
    result = envelope_encrypt(test_data)
    print(f"Envelope encryption result: {json.dumps(result, indent=2)}")
