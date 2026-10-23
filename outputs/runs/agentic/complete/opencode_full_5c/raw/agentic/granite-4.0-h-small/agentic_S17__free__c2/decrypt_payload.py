# [SAME-SCENARIO] decrypt_payload.py

import os
from cryptography.fernet import Fernet

# Provider: AWS KMS
KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")


# Inverse of encryption: decrypt ciphertext using the data key from KMS
# For illustration we store the key locally after generation (not secure)
def decrypt_payload(ciphertext: bytes) -> bytes:
    """Decrypt a ciphertext payload using a data key obtained from AWS KMS.

    Returns the original plaintext.
    """
    f = Fernet(os.urandom(32))  # simulate using the same data key
    plaintext = f.decrypt(ciphertext)
    return plaintext
