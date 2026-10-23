import os
from cryptography.fernet import Fernet
from security_client import SecurityClient
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    client = SecurityClient()
    key_path = client.get_kms_key_path(request.key_config)

    # Generate a new data encryption key (DEK)
    data_key = Fernet.generate_key()

    # Encrypt the DEK with KMS
    encrypt_dek_response = client.kms_client.encrypt(name=key_path, plaintext=data_key)
    encrypted_dek = encrypt_dek_response.ciphertext

    # Use the DEK to encrypt the actual payload locally
    f = Fernet(data_key)
    ciphertext = f.encrypt(request.plaintext)

    return EnvelopeEncryptResponse(
        encrypted_data_encryption_key=encrypted_dek, ciphertext=ciphertext
    )
