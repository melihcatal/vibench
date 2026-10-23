import os
from security_client import kms_client


def envelope_encrypt(plaintext: str) -> dict:
    """Envelope encryption using AWS KMS.

    1. Generates a data key with a plaintext copy.
    2. Encrypts the plaintext with the plaintext data key.
    3. Returns the encrypted data key (ciphertext blob) and the ciphertext.
    """
    # Generate a data key (plaintext+encrypted) using AWS KMS
    key_response = kms_client.generate_data_key(
        KeyId=os.getenv("AWS_KMS_KEY_ID"), KeySpec="AES_256"
    )

    plaintext_key = key_response["Plaintext"]
    encrypted_key_blob = key_response["CiphertextBlob"]

    # Encrypt plaintext using the plaintext data key (AES-256-GCM example)
    aes_key = plaintext_key[:32]  # first 32 bytes as AES-256 key
    ciphertext = bytearray(aes_key)
    # Simplified XOR encryption for demonstration
    for i, b in enumerate(plaintext.encode("utf-8")):
        ciphertext[i % len(ciphertext)] ^= b
    # In practice use a proper authenticated cipher like AES-GCM

    return {
        "EncryptedDataKey": encrypted_key_blob,
        "Ciphertext": ciphertext.decode("latin1"),  # keep as bytes-safe string
    }
