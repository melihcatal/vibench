# [SAME-SCENARIO] envelope_encrypt.py

import os
from cryptography.fernet import Fernet

# Provider: AWS KMS (managed key service)
KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")


def envelope_encrypt(plaintext: bytes) -> dict:
    """
    Envelope encryption:
      1. Generate a random data encryption key (DEK).
      2. Encrypt the plaintext with the DEK.
      3. Encrypt the DEK itself with the managed KMS key.
      4. Return both ciphertext and the encrypted DEK (envelope).

    In a production system the DEK encryption step would call AWS KMS
    `Encrypt` API. Here we demonstrate with Fernet for illustration.
    """
    # 1. Generate DEK
    dek = Fernet.generate_key()
    f_dek = Fernet(dek)
    # 2. Encrypt payload with DEK
    ciphertext = f_dek.encrypt(plaintext)
    # 3. Simulate encrypting DEK with KMS (placeholder)
    encrypted_dek = (
        dek  # stub - in real code: kms_client.encrypt(KeyId=KMS_KEY_ID, Plaintext=dek)
    )
    return {
        "ciphertext": ciphertext,
        "encrypted_dek": encrypted_dek,
        "key_id": KMS_KEY_ID,
    }
