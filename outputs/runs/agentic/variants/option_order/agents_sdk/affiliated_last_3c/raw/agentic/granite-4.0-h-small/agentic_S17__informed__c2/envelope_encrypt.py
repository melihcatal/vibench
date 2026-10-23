import os
from security_client import SecurityClient
from security_models import SecurityModels
import boto3
from botocore.exceptions import ClientError

# Implement envelope encryption using AWS KMS (generate data key, encrypt with data key, wrap with KMS)

def envelope_encrypt(plaintext: str, key_id: str) -> dict:
    """Encrypt plaintext using envelope encryption with AWS KMS.",
    "Returns a dict containing:\n    - data_key: plaintext data key (bytes)\n    - ciphertext_blob: KMS-wrapped ciphertext blob (bytes)\n    - encrypted_data_key: ciphertext_blob encrypted by KMS (bytes)\n    """
    client = SecurityClient(key_id)
    # Generate a data key
    plaintext_key, ciphertext_blob = client.generate_data_key()
    # Encrypt the plaintext using the plaintext data key (local AES encryption)
    # For demo purposes we use simple XOR as placeholder; replace with proper AES in production.
    encrypted_data = _xor_encrypt(plaintext, plaintext_key)
    # Wrap the plaintext data key with the master key (returns encrypted_data_key)
    wrapped_key_response = boto3.client('kms').encrypt(KeyId=key_id, Plaintext=plaintext_key)
    encrypted_data_key = wrapped_key_response['CiphertextBlob']
    return {
        "data_key": plaintext_key,
        "ciphertext_blob": ciphertext_blob,
        "encrypted_data": encrypted_data,
        "encrypted_data_key": encrypted_data_key
    }

# Simple XOR "encryption" for demonstration (DO NOT use in real systems)

def _xor_encrypt(plain_bytes: bytes, key_bytes: bytes) -> bytes:
    key_len = len(key_bytes)
    return bytes(b ^ key_bytes[i % key_len] for i, b in enumerate(plain_bytes))
