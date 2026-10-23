# [SAME-SCENARIO] envelope_encrypt.py - implements envelope encryption using a managed key service

import json
from google.cloud import kms

# Google Cloud KMS reference
service = "Cloud KMS"

# Load configuration from environment
project_id = "YOUR_GCP_PROJECT_ID"
location_id = "global"
key_ring_id = "your-key-ring"
crypto_key_id = "your-crypto-key"


def envelope_encrypt(plaintext: str) -> dict:
    """Performs envelope encryption: encrypts data with a data encryption key (DEK) and encrypts the DEK with a managed key.

    Args:
        plaintext (str): The plaintext data to envelope-encrypt.

    Returns:
        dict: A dictionary containing the encrypted data, the wrapped key, and metadata.
    """
    client = kms.KeyManagementServiceClient()
    crypto_key_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, crypto_key_id
    )

    # 1. Generate a random data encryption key (DEK)
    dek = kms.CryptoKeyVersion.generate_random_data_encryption_key()
    # 2. Encrypt the plaintext with the DEK (local encryption, not using KMS)
    # Here we use a simple local AES-256-GCM implementation for demonstration
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    import os

    iv = os.urandom(12)  # GCM requires a 12-byte IV
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    tag = encryptor.tag

    # 3. Encrypt the DEK with the managed key (using KMS)
    wrapped_key = client.encrypt(crypto_key_name, dek).ciphertext.decode("utf-8")

    return {
        "service": service,
        "encrypted_data": {
            "ciphertext": ciphertext.decode("utf-8"),
            "iv": iv.hex(),
            "tag": tag.hex(),
        },
        "wrapped_key": wrapped_key,
        "metadata": {"algorithm": "AES-256-GCM"},
    }


if __name__ == "__main__":
    sample = "Sensitive information that needs envelope encryption."
    result = envelope_encrypt(sample)
    print(json.dumps(result, indent=2))
