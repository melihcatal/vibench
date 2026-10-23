from security_client import SecurityClient
from security_models import EncryptionRequest, EncryptionResponse
import base64


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """Encrypts a plaintext payload with a managed key using Google Cloud KMS."""
    client = SecurityClient()

    # The resource name of the CryptoKey
    key_name = request.key_name
    plaintext_bytes = request.plaintext.encode("utf-8")

    # Call the KMS API to encrypt the data
    # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS
    encrypt_response = client.kms_client.encrypt(
        name=key_name, plaintext=plaintext_bytes
    )

    # The ciphertext is base64 encoded for easy storage/transfer
    ciphertext = base64.b64encode(encrypt_response.ciphertext).decode("utf-8")

    return EncryptionResponse(ciphertext=ciphertext, key_name=key_name)
