import os
from security_client import KeyManagementClient

# Decrypt a ciphertext payload with the managed key used for encryption


def decrypt_payload(ciphertext: bytes, key_name: str) -> str:
    """Decrypt ciphertext using the specified managed key.
    Returns the original plaintext string.
    """
    client = KeyManagementClient(service="google-cloud-kms")
    plaintext_bytes = client.decrypt(key_name, ciphertext)
    return plaintext_bytes.decode()


if __name__ == "__main__":
    encrypted = b"CIPHERTEXT_FROM_PREVIOUS_STEP"
    key_id = os.getenv("KMS_KEY_ID")
    plaintext = decrypt_payload(encrypted, key_id)
    print("Decrypted:", plaintext)
