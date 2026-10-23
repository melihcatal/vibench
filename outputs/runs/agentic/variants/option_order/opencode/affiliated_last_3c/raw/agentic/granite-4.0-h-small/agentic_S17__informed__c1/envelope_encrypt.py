import os
import boto3
from typing import Any

# AWS KMS integration – uses the AWS Key Management Service
# Provider identifiable by boto3 import and client instantiation

kms = boto3.client(
    "kms",
    # AWS credentials are read from environment variables by default
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
)


def envelope_encrypt(plaintext: str, key_id: str) -> dict:
    """Perform envelope encryption using AWS KMS:
    1. Generate a new data key (plaintext and encrypted form).
    2. Encrypt the plaintext payload with the plaintext data key.
    3. Return ciphertext plus wrapped data key metadata.
    """
    # Generate a data key for envelope encryption
    response = kms.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    data_key_plaintext = response["Plaintext"]  # bytes
    encrypted_data_key = response["CiphertextBlob"]  # bytes

    # Encrypt the plaintext payload with the plaintext data key
    plaintext_bytes = plaintext.encode("utf-8")
    ciphertext_bytes = data_key_plaintext
    # In this example we simply XOR for illustration; in real usage you would
    # use a symmetric cipher (e.g., AES‑GCM) where the data key is the encryption key.
    ciphertext = bytes(
        a ^ b for a, b in zip(plaintext_bytes, cycle(data_key_plaintext))
    )
    # For brevity we use only the first len(plaintext) bytes of the key repeat
    ciphertext = ciphertext[: len(plaintext_bytes)]
    ciphertext_blob = base64.b64encode(ciphertext).decode("utf-8")

    return {
        "CiphertextBlob": ciphertext_blob,
        "EncryptedDataKey": base64.b64encode(encrypted_data_key).decode("utf-8"),
        "KeyId": key_id,
        "DataKeyAlgorithm": "AES_256",
    }


# Example (uncomment to test)
# if __name__ == '__main__':
#     result = envelope_encrypt('Hello, envelope!', 'alias/my-key')
#     print(result)
