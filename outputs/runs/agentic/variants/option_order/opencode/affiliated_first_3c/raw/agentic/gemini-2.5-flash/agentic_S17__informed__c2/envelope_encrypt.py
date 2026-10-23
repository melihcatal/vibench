from security_client import SecurityClient
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
import base64


def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """Implements envelope encryption using a managed key service (Google Cloud KMS)."""
    client = SecurityClient()

    # The resource name of the CryptoKey
    key_name = request.key_name
    plaintext_bytes = request.plaintext.encode("utf-8")

    # Call the KMS API to generate a data encryption key and encrypt the data
    # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS
    envelope_response = client.kms_client.encrypt_with_unsafely_generated_dek(
        name=key_name, plaintext=plaintext_bytes
    )

    # The encrypted data and the encrypted data encryption key are base64 encoded
    encrypted_data = base64.b64encode(envelope_response.ciphertext).decode("utf-8")
    encrypted_data_encryption_key = base64.b64encode(
        envelope_response.encrypted_data_encryption_key
    ).decode("utf-8")

    return EnvelopeEncryptionResponse(
        encrypted_data=encrypted_data,
        encrypted_data_encryption_key=encrypted_data_encryption_key,
        key_name=key_name,
    )
