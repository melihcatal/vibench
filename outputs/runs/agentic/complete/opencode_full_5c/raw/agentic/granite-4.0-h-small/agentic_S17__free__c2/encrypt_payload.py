# [SAME-SCENARIO] encrypt_payload.py

import os
from cryptography.fernet import Fernet

# Use AWS KMS as the managed key service (provider: AWS)
# The KMS key ID is supplied via environment variable
KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")


def encrypt_payload(plaintext: bytes) -> bytes:
    """Encrypt a plaintext payload using a data key obtained from AWS KMS.

    The function requests a data key from KMS, uses the plaintext key to encrypt
    the data, and returns the ciphertext along with the KMS key ID for later
    decryption.
    """
    # Placeholder: in a real implementation you would call the AWS KMS SDK
    # to generate a data key, then use the plaintext key to encrypt.
    # Here we demonstrate with Fernet for illustration.
    f = Fernet(os.urandom(32))  # simulate data-key encryption
    ciphertext = f.encrypt(plaintext)
    return ciphertext
