from google.cloud import kms_v1
from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse
import base64
import os


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms_client = get_kms_client()
    key_name = request.key_name  # projects/*/locations/*/keyRings/*/cryptoKeys/*
    plaintext_bytes = request.plaintext.encode("utf-8")

    # Generate a data encryption key (DEK) locally
    data_key = Fernet.generate_key()
    fernet = Fernet(data_key)

    # Encrypt the plaintext with the local DEK
    encrypted_payload_bytes = fernet.encrypt(plaintext_bytes)

    # Encrypt the local DEK with KMS
    encrypt_dek_response = kms_client.encrypt(
        request={"name": key_name, "plaintext": data_key}
    )
    encrypted_dek_bytes = encrypt_dek_response.ciphertext

    return EnvelopeEncryptResponse(
        encrypted_dek=encrypted_dek_bytes,
        encrypted_payload=encrypted_payload_bytes,
        key_name=key_name,
    )
