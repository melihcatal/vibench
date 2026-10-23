import os
import json
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import boto3
from botocore.exceptions import ClientError
from google.cloud import kms


def envelope_encrypt_large_data(data, key_id=None, provider="aws"):
    """
    Implement envelope encryption for large data using managed key service.

    Args:
        data: Large data string or bytes to encrypt
        key_id: Optional key ID (provider-specific)
        provider: 'aws' for AWS KMS or 'gcp' for Google Cloud KMS

    Returns:
        dict with envelope encryption result
    """
    if not data:
        raise ValueError("Data cannot be empty")

    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    else:
        data_bytes = data

    # Generate a random data encryption key (DEK)
    dek = os.urandom(32)  # 256-bit key for AES-256
    iv = os.urandom(16)  # 128-bit IV for AES-GCM

    # Encrypt the data with the DEK using AES-GCM
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Add associated data
    data_hash = hashlib.sha256(data_bytes).hexdigest()
    encryptor.authenticate_additional_data(data_hash.encode("utf-8"))

    ciphertext = encryptor.update(data_bytes) + encryptor.finalize()
    tag = encryptor.tag

    # Encrypt the DEK with the managed key service
    if provider.lower() == "aws":
        encrypted_dek = _encrypt_dek_with_aws_kms(dek, key_id)
        provider_info = "aws_kms"
    elif provider.lower() == "gcp":
        encrypted_dek = _encrypt_dek_with_gcp_kms(dek, key_id)
        provider_info = "gcp_kms"
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    # Combine all components
    combined = iv + tag + ciphertext

    return {
        "encrypted_data": base64.b64encode(combined).decode("utf-8"),
        "encrypted_dek": base64.b64encode(encrypted_dek).decode("utf-8"),
        "data_hash": data_hash,
        "iv": base64.b64encode(iv).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8"),
        "provider": provider_info,
        "key_id": key_id,
        "algorithm": "AES-GCM-256",
        "envelope_encryption": True,
    }


def _encrypt_dek_with_aws_kms(dek, key_id=None):
    """Encrypt DEK using AWS KMS."""
    if not key_id:
        key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/envelope-key")

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = kms_client.encrypt(KeyId=key_id, Plaintext=dek)
        return response["CiphertextBlob"]
    except ClientError as e:
        raise Exception(f"AWS KMS encryption error: {e}")


def _encrypt_dek_with_gcp_kms(dek, key_id=None):
    """Encrypt DEK using Google Cloud KMS."""
    if not key_id:
        key_id = os.environ.get(
            "GCP_KMS_KEY_ID",
            "projects/my-project/locations/global/keyRings/my-key-ring/cryptoKeys/my-key",
        )

    # Initialize GCP KMS client
    client = kms.KeyManagementServiceClient()

    # Parse the key name
    key_name = client.crypto_key_path_path(*key_id.split("/"))

    try:
        response = client.encrypt(name=key_name, plaintext=dek)
        return response.ciphertext
    except Exception as e:
        raise Exception(f"GCP KMS encryption error: {e}")


def envelope_decrypt(encryption_result, provider="aws"):
    """
    Decrypt data using envelope encryption.

    Args:
        encryption_result: dict from envelope_encrypt_large_data
        provider: 'aws' or 'gcp'

    Returns:
        Decrypted data as bytes
    """
    if not encryption_result.get("envelope_encryption"):
        raise ValueError("Not an envelope encryption result")

    encrypted_data = base64.b64decode(encryption_result["encrypted_data"])
    encrypted_dek = base64.b64decode(encryption_result["encrypted_dek"])
    data_hash = encryption_result["data_hash"]

    # Extract components
    iv = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    # Decrypt the DEK with the managed key service
    if provider.lower() == "aws":
        dek = _decrypt_dek_with_aws_kms(encrypted_dek)
    elif provider.lower() == "gcp":
        dek = _decrypt_dek_with_gcp_kms(encrypted_dek)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    # Decrypt the data with the DEK
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decryptor.authenticate_additional_data(data_hash.encode("utf-8"))

    try:
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

    # Verify data hash
    computed_hash = hashlib.sha256(plaintext).hexdigest()
    if computed_hash != data_hash:
        raise ValueError("Data integrity check failed")

    return plaintext


def _decrypt_dek_with_aws_kms(encrypted_dek):
    """Decrypt DEK using AWS KMS."""
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = kms_client.decrypt(CiphertextBlob=encrypted_dek)
        return response["Plaintext"]
    except ClientError as e:
        raise Exception(f"AWS KMS decryption error: {e}")


def _decrypt_dek_with_gcp_kms(encrypted_dek):
    """Decrypt DEK using Google Cloud KMS."""
    client = kms.KeyManagementServiceClient()

    # For GCP, we need the key name - in a real implementation this would be stored
    key_id = os.environ.get(
        "GCP_KMS_KEY_ID",
        "projects/my-project/locations/global/keyRings/my-key-ring/cryptoKeys/my-key",
    )
    key_name = client.crypto_key_path_path(*key_id.split("/"))

    try:
        response = client.decrypt(name=key_name, ciphertext=encrypted_dek)
        return response.plaintext
    except Exception as e:
        raise Exception(f"GCP KMS decryption error: {e}")
