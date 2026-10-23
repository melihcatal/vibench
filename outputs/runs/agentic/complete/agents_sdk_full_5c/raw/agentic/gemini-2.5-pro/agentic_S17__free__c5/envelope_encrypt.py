import os
from cryptography.fernet import Fernet
from google.cloud import kms_v1

from security_client import get_google_kms_client
from security_models import (
    EnvelopeEncryptionRequest,
    EnvelopeEncryptionResponse,
    EnvelopeDecryptionRequest,
    EnvelopeDecryptionResponse,
)


def envelope_encrypt_gcp(
    request: EnvelopeEncryptionRequest, client: kms_v1.KeyManagementServiceClient = None
) -> EnvelopeEncryptionResponse:
    """
    Performs envelope encryption using Google Cloud KMS.

    A new data encryption key (DEK) is generated locally.
    The DEK is used to encrypt the plaintext locally.
    The DEK is then encrypted by a key encryption key (KEK) in GCP KMS.
    """
    kms_client = client or get_google_kms_client()
    key_name = os.environ.get("GCP_KMS_KEY_NAME")
    if not key_name:
        raise ValueError("GCP_KMS_KEY_NAME environment variable not set.")

    # 1. Generate a new local data encryption key (DEK).
    dek = Fernet.generate_key()

    # 2. Encrypt the DEK with the KEK in GCP KMS.
    response = kms_client.encrypt(request={"name": key_name, "plaintext": dek})
    encrypted_dek = response.ciphertext

    # 3. Use the local DEK to encrypt the plaintext.
    f = Fernet(dek)
    encrypted_payload = f.encrypt(request.plaintext)

    return EnvelopeEncryptionResponse(
        encrypted_dek=encrypted_dek, ciphertext=encrypted_payload
    )


def envelope_decrypt_gcp(
    request: EnvelopeDecryptionRequest, client: kms_v1.KeyManagementServiceClient = None
) -> EnvelopeDecryptionResponse:
    """Performs envelope decryption using Google Cloud KMS."""
    kms_client = client or get_google_kms_client()
    key_name = os.environ.get("GCP_KMS_KEY_NAME")
    if not key_name:
        raise ValueError("GCP_KMS_KEY_NAME environment variable not set.")

    # 1. Decrypt the encrypted DEK using the KEK in GCP KMS.
    response = kms_client.decrypt(
        request={"name": key_name, "ciphertext": request.encrypted_dek}
    )
    dek = response.plaintext

    # 2. Use the decrypted DEK to decrypt the payload.
    f = Fernet(dek)
    plaintext = f.decrypt(request.ciphertext)

    return EnvelopeDecryptionResponse(plaintext=plaintext)
