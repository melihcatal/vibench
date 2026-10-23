import base64
import os
import boto3
from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    EnvelopeDecryptionRequest,
    EnvelopeDecryptionResponse,
)


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """Implements envelope encryption using AWS KMS."""
    kms_client = get_kms_client()

    # Generate a data key and its encrypted version using KMS
    generate_data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id, KeySpec="AES_256"
    )

    plaintext_data_key = generate_data_key_response["Plaintext"]
    encrypted_data_key = generate_data_key_response["CiphertextBlob"]

    # Use the plaintext data key for local symmetric encryption
    # Fernet requires a URL-safe base64-encoded key of 32 bytes.
    # KMS AES_256 data key is 32 bytes, so it fits directly after base64 encoding.
    fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
    fernet = Fernet(fernet_key)

    encrypted_payload = fernet.encrypt(request.plaintext_payload)

    # It's crucial to destroy the plaintext data key after use
    # In a real application, ensure this is handled securely, e.g., by overwriting memory
    # Python's garbage collection handles memory, but for extremely sensitive keys, more explicit measures might be considered.

    return EnvelopeEncryptionResponse(
        encrypted_data_key=base64.b64encode(encrypted_data_key),
        encrypted_payload=encrypted_payload,
        key_id=request.key_id,
    )


def envelope_decrypt(request: EnvelopeDecryptionRequest) -> EnvelopeDecryptionResponse:
    """Decrypts an envelope encrypted payload using AWS KMS."""
    kms_client = get_kms_client()

    # Decrypt the encrypted data key using KMS
    decrypt_data_key_response = kms_client.decrypt(
        CiphertextBlob=base64.b64decode(request.encrypted_data_key),
        KeyId=request.key_id,
    )

    plaintext_data_key = decrypt_data_key_response["Plaintext"]

    # Use the plaintext data key for local symmetric decryption
    fernet_key = base64.urlsafe_b64encode(plaintext_data_key)
    fernet = Fernet(fernet_key)

    plaintext_payload = fernet.decrypt(request.encrypted_payload)

    # Destroy the plaintext data key after use

    return EnvelopeDecryptionResponse(
        plaintext_payload=plaintext_payload, key_id=request.key_id
    )
