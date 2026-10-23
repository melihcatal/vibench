from security_client import SecurityClient
from security_models import EnvelopeEncryptionResponse
from cryptography.fernet import Fernet
import base64


def envelope_encrypt(plaintext_payload: bytes, key_id: str, region: str, encryption_context: dict = None) -> EnvelopeEncryptionResponse:
    security_client = SecurityClient(region_name=region)
    response = EnvelopeEncryptionResponse()
    try:
        # Generate a data key from KMS
        data_key_response = security_client.generate_data_key(
            key_id=key_id,
            key_spec="AES_256",
            encryption_context=encryption_context
        )
        plaintext_data_key = data_key_response["Plaintext"]
        encrypted_data_key = data_key_response["CiphertextBlob"]

        # Use the plaintext data key to encrypt the actual payload
        # Fernet requires a URL-safe base64-encoded key
        fernet_key = base64.urlsafe_b64encode(plaintext_data_key[:32]) # Fernet uses 32-byte key
        f = Fernet(fernet_key)
        ciphertext = f.encrypt(plaintext_payload)

        response.ciphertext_blob = ciphertext
        response.encrypted_data_key = encrypted_data_key
        response.plaintext = plaintext_data_key # For demonstration, in real scenario, this would not be returned

    except Exception as e:
        response.error = str(e)
    return response
