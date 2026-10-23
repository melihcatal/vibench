import os
from cryptography.fernet import Fernet
from security_client import get_gcp_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
import base64

def envelope_encrypt_data(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """
    Performs envelope encryption on a plaintext payload using Google Cloud KMS.
    """
    kms_client = get_gcp_kms_client()

    key_path = os.environ.get("GCP_KMS_KEY_NAME")
    if not key_path:
        raise ValueError("GCP_KMS_KEY_NAME environment variable is not set.")

    # 1. Generate a local, symmetric data encryption key (DEK)
    data_key = Fernet.generate_key()

    # 2. Encrypt the DEK with the Cloud KMS key (KEK)
    encrypt_response = kms_client.encrypt(
        request={"name": key_path, "plaintext": data_key}
    )
    encrypted_data_key = encrypt_response.ciphertext

    # 3. Encrypt the plaintext data with the local DEK
    f = Fernet(data_key)
    encrypted_payload = f.encrypt(request.plaintext)

    return EnvelopeEncryptionResponse(
        encrypted_payload=base64.b64encode(encrypted_payload).decode('utf-8'),
        encrypted_data_key=base64.b64encode(encrypted_data_key).decode('utf-8')
    )
