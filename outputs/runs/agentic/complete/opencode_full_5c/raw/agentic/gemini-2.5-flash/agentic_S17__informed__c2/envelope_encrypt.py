from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
import os
import base64
from cryptography.fernet import Fernet


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """Implements envelope encryption using Google Cloud KMS for the data key.

    Args:
        request: An EnvelopeEncryptionRequest object containing the plaintext and KMS key ID.

    Returns:
        An EnvelopeEncryptionResponse object with the encrypted data key, ciphertext, and KMS key ID.
    """
    kms_client = get_kms_client()
    full_key_path = request.key_id

    try:
        # 1. Generate a new data encryption key (DEK) locally
        data_key = Fernet.generate_key()
        f = Fernet(data_key)

        # 2. Encrypt the data key (DEK) with Google Cloud KMS
        # The KMS encrypt method expects bytes for plaintext
        encrypted_data_key_response = kms_client.encrypt(
            name=full_key_path, plaintext=data_key
        )
        encrypted_data_key_b64 = base64.b64encode(
            encrypted_data_key_response.ciphertext
        ).decode("utf-8")

        # 3. Encrypt the actual payload with the locally generated DEK
        plaintext_bytes = request.plaintext.encode("utf-8")
        ciphertext_payload = f.encrypt(plaintext_bytes)
        ciphertext_payload_b64 = base64.b64encode(ciphertext_payload).decode("utf-8")

        return EnvelopeEncryptionResponse(
            encrypted_data_key=encrypted_data_key_b64,
            ciphertext=ciphertext_payload_b64,
            key_id=request.key_id,
        )
    except Exception as e:
        raise RuntimeError(
            f"Error performing envelope encryption with Google Cloud KMS: {e}"
        )
