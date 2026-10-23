import base64
import os
from cryptography.fernet import Fernet
from google.cloud import kms
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
from security_client import KmsClient

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    kms_client = KmsClient()
    client = kms_client.client

    # 1. Generate a new data encryption key (DEK)
    data_encryption_key = Fernet.generate_key()

    # 2. Encrypt the DEK with the KMS key
    key_name = kms_client.get_key_path(request.project_id, request.location, request.key_ring, request.key_id)
    encrypt_dek_response = client.encrypt(request={"name": key_name, "plaintext": data_encryption_key})
    encrypted_data_encryption_key = encrypt_dek_response.ciphertext

    # 3. Use the DEK to encrypt the plaintext payload
    f = Fernet(data_encryption_key)
    ciphertext = f.encrypt(request.plaintext.encode('utf-8'))

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_data_encryption_key=encrypted_data_encryption_key
    )
