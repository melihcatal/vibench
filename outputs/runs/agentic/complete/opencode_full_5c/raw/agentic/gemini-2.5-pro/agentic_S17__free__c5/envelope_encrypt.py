import os
from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """Implements envelope encryption using a GCP KMS key to wrap a local data key."""
    # 1. Generate a local data encryption key (DEK).
    dek = Fernet.generate_key()

    # 2. Encrypt the plaintext with the DEK.
    f = Fernet(dek)
    ciphertext = f.encrypt(request.plaintext)

    # 3. Wrap the DEK with the KMS key.
    kms_client = get_kms_client()
    kms_response = kms_client.encrypt(
        request={"name": request.key_name, "plaintext": dek}
    )
    wrapped_dek = kms_response.ciphertext

    return EnvelopeEncryptionResponse(wrapped_dek=wrapped_dek, ciphertext=ciphertext)
