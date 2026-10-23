import os
import base64
from cryptography.fernet import Fernet
from google.cloud import kms_v1
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    client = kms_v1.KeyManagementServiceClient()
    key_name = request.key_name
    plaintext_bytes = request.plaintext.encode("utf-8")

    try:
        # Generate a new data encryption key (DEK) for local encryption
        data_key = Fernet.generate_key()
        fernet = Fernet(data_key)
        encrypted_data = fernet.encrypt(plaintext_bytes)

        # Encrypt the data key with Google Cloud KMS
        # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; auth=GOOGLE_APPLICATION_CREDENTIALS
        encrypt_dek_response = client.encrypt(
            request={"name": key_name, "plaintext": data_key}
        )
        encrypted_data_key = base64.b64encode(encrypt_dek_response.ciphertext).decode(
            "utf-8"
        )

        return EnvelopeEncryptionResponse(
            encrypted_data=base64.b64encode(encrypted_data).decode("utf-8"),
            encrypted_data_key=encrypted_data_key,
        )
    except Exception as e:
        raise RuntimeError(f"Envelope encryption failed: {e}")


def envelope_decrypt(request: EnvelopeEncryptionResponse, key_name: str) -> str:
    client = kms_v1.KeyManagementServiceClient()

    try:
        # Decrypt the encrypted data key with Google Cloud KMS
        # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; auth=GOOGLE_APPLICATION_CREDENTIALS
        decrypt_dek_response = client.decrypt(
            request={
                "name": key_name,
                "ciphertext": base64.b64decode(request.encrypted_data_key),
            }
        )
        data_key = decrypt_dek_response.plaintext

        # Decrypt the data locally with the decrypted data key
        fernet = Fernet(data_key)
        decrypted_data = fernet.decrypt(base64.b64decode(request.encrypted_data))

        return decrypted_data.decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Envelope decryption failed: {e}")
