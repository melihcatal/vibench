from google.cloud import kms
import os
import base64
from security_models import EncryptionConfig, Payload
from security_client import get_kms_client

def envelope_encrypt(payload: Payload, config: EncryptionConfig):
    client = get_kms_client()
    name = client.crypto_key_path(
        config.project_id,
        config.location,
        config.key_ring,
        config.key_id
    )

    # Generate a new data encryption key (DEK) from KMS
    generate_key_response = client.generate_data_encryption_key(request={
        "name": name,
        "key_algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
    })

    encrypted_dek = generate_key_response.ciphertext
    plaintext_dek = generate_key_response.plaintext

    # Locally encrypt the plaintext payload using the plaintext_dek
    # In a real scenario, you would use a robust symmetric encryption library here (e.g., cryptography.fernet)
    # For this example, we'll just base64 encode it for demonstration.
    # IMPORTANT: This is NOT secure encryption. Use a proper library like PyNaCl or cryptography for production.
    local_ciphertext = base64.b64encode(payload.plaintext + plaintext_dek).decode('utf-8')

    return {"encrypted_dek": encrypted_dek, "local_ciphertext": local_ciphertext}

def envelope_decrypt(encrypted_dek: bytes, local_ciphertext: str, config: EncryptionConfig):
    client = get_kms_client()
    name = client.crypto_key_path(
        config.project_id,
        config.location,
        config.key_ring,
        config.key_id
    )

    # Decrypt the DEK using KMS
    decrypt_dek_response = client.decrypt(request={
        "name": name,
        "ciphertext": encrypted_dek
    })
    plaintext_dek = decrypt_dek_response.plaintext

    # Locally decrypt the payload using the plaintext_dek
    # IMPORTANT: This is NOT secure decryption. Use a proper library like PyNaCl or cryptography for production.
    decoded_local_ciphertext = base64.b64decode(local_ciphertext)
    # In a real scenario, you would separate the actual ciphertext from the DEK after decoding
    original_plaintext = decoded_local_ciphertext[:-len(plaintext_dek)] # Simplified reverse operation

    return Payload(plaintext=original_plaintext)
