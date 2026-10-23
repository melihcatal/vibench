import os
from cryptography.fernet import Fernet
from google.cloud import kms
from security_client import get_gcp_kms_client

def envelope_encrypt_gcp(
    plaintext: bytes,
    key_name: str
) -> tuple[bytes, bytes]:
    """
    Performs envelope encryption using a local data key and a Google Cloud KMS key.

    Args:
        plaintext: The data to encrypt.
        key_name: The resource name of the GCP KMS key.
                  (e.g., projects/PROJECT/locations/LOCATION/keyRings/RING/cryptoKeys/KEY)

    Returns:
        A tuple containing the encrypted data key and the ciphertext.
    """
    # 1. Generate a local data encryption key (DEK).
    dek = Fernet.generate_key()

    # 2. Encrypt the DEK with the GCP KMS key (KEK).
    kms_client = get_gcp_kms_client()
    # Provider-specific integration with Google Cloud KMS
    encrypt_response = kms_client.encrypt(
        request={"name": key_name, "plaintext": dek}
    )
    encrypted_dek = encrypt_response.ciphertext

    # 3. Use the local DEK to encrypt the plaintext.
    f = Fernet(dek)
    ciphertext = f.encrypt(plaintext)

    return encrypted_dek, ciphertext
