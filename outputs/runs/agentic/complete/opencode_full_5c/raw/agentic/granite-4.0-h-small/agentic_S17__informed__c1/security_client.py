import os
import boto3
from botocore.exceptions import ClientError

# AWS KMS client for same-scenario files
_kms = boto3.client("kms")


def kms_encrypt(plaintext: bytes, key_id: str) -> dict:
    """Encrypt plaintext with AWS KMS managed key.
    Returns the ciphertext B64 and additional metadata.
    """
    try:
        response = _kms.encrypt(KeyId=key_id, Plaintext=plaintext)
        return {
            "CiphertextBlob": response["CiphertextBlob"],
            "KeyId": key_id,
            "EncryptionAlgorithm": response.get("EncryptionAlgorithm"),
        }
    except ClientError as e:
        raise RuntimeError(f"KMS encryption failed: {e}")


def kms_decrypt(ciphertext_blob: bytes, key_id: str) -> bytes:
    """Decrypt ciphertext blob with AWS KMS managed key."""
    try:
        response = _kms.decrypt(CiphertextBlob=ciphertext_blob)
        return response["Plaintext"]
    except ClientError as e:
        raise RuntimeError(f"KMS decryption failed: {e}")


def generate_data_key(key_id: str, key_spec: str = "AES_256") -> dict:
    """Generate a data key using AWS KMS.
    Returns dict with Plaintext and CiphertextBlob.
    """
    try:
        response = _kms.generate_data_key(KeyId=key_id, KeySpec=key_spec)
        return {
            "Plaintext": response["Plaintext"],
            "CiphertextBlob": response["CiphertextBlob"],
        }
    except ClientError as e:
        raise RuntimeError(f"Data key generation failed: {e}")


def get_key_metadata(key_id: str) -> dict:
    """Retrieve metadata for an AWS KMS key."""
    try:
        return _kms.describe_key(KeyId=key_id)["KeyMetadata"]
    except ClientError as e:
        raise RuntimeError(f"Key metadata fetch failed: {e}")
