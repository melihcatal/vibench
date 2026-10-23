import os
from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest
from google.cloud import kms_v1


def envelope_encrypt(request: EnvelopeEncryptRequest) -> tuple[bytes, bytes]:
    # Generate a new data encryption key (DEK) locally
    dek = Fernet.generate_key()
    f = Fernet(dek)

    # Encrypt the plaintext with the local DEK
    encrypted_payload = f.encrypt(request.plaintext)

    # Encrypt the DEK with Google Cloud KMS
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id,
        request.location_id,
        request.key_ring_id,
        request.crypto_key_id,
    )

    # Google Cloud KMS signal: google.cloud.kms_v1.KeyManagementServiceClient
    # Google Cloud KMS signal: client.crypto_key_path
    encrypt_dek_response = client.encrypt(
        request=kms_v1.EncryptRequest(name=key_name, plaintext=dek)
    )
    encrypted_dek = encrypt_dek_response.ciphertext

    return encrypted_dek, encrypted_payload
