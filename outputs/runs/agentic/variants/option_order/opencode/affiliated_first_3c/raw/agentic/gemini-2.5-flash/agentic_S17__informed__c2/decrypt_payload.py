from security_client import SecurityClient
from security_models import DecryptionRequest, DecryptionResponse
import base64


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """Decrypts a ciphertext payload with a managed key using Google Cloud KMS."""
    client = SecurityClient()

    # The resource name of the CryptoKey
    key_name = request.key_name
    ciphertext_bytes = base64.b64decode(request.ciphertext)

    # Call the KMS API to decrypt the data
    # Google Cloud KMS: service=Cloud KMS; sdk=google-cloud-kms; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS
    decrypt_response = client.kms_client.decrypt(
        name=key_name, ciphertext=ciphertext_bytes
    )

    plaintext = decrypt_response.plaintext.decode("utf-8")

    return DecryptionResponse(plaintext=plaintext, key_name=key_name)
