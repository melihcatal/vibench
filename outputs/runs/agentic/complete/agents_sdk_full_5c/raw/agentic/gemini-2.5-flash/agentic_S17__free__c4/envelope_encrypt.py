
"""
envelope_encrypt.py - implements envelope encryption using a managed key service (Google Cloud KMS) to encrypt a Data Encryption Key (DEK).
"""

import os
from security_client import KmsClient
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse
from google.cloud import kms_v1 # Provider-identifying signal

def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms_client = KmsClient()
    key_name = kms_client.get_key_name(request.project_id, request.location_id, request.key_ring_id, request.key_id)

    # 1. Generate a new Data Encryption Key (DEK) locally (e.g., a random symmetric key).
    # For a real implementation, this would be a strong random key.
    # Using a fixed size for demonstration purposes. A real DEK would typically be 16, 24, or 32 bytes for AES.
    data_encryption_key = os.urandom(32) # Example 32-byte (256-bit) AES key

    # 2. Encrypt the DEK with Google Cloud KMS.
    # The KMS API hostname is kms.googleapis.com, implicitly used by the client.
    encrypt_dek_response = kms_client.client.encrypt(
        name=key_name,
        plaintext=data_encryption_key
    )
    encrypted_dek = encrypt_dek_response.ciphertext

    # 3. Use the (unencrypted) DEK to encrypt the actual plaintext_data locally.
    # This is a placeholder for actual symmetric encryption (e.g., AES GCM).
    # For this exercise, we'll simply prepend a small marker and XOR for demonstration
    # This is NOT a secure encryption method. In a real scenario, use a library like cryptography.fernet
    encrypted_data = b'ENC_DATA_PLACEHOLDER_' + bytes([b ^ d for b, d in zip(request.plaintext_data, data_encryption_key * (len(request.plaintext_data) // len(data_encryption_key) + 1))])[:len(request.plaintext_data)]

    return EnvelopeEncryptResponse(encrypted_data=encrypted_data, encrypted_dek=encrypted_dek)
