import base64
from security_client import KMSClient
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = KMSClient().get_client()
    # The resource name of the CryptoKey to use for encryption.
    # e.g. 'projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/keyRings/YOUR_KEY_RING_NAME/cryptoKeys/YOUR_KEY_NAME'
    # The plaintext to be encrypted.
    plaintext_bytes = request.plaintext.encode('utf-8')

    # Call the KMS API to encrypt the plaintext.
    response = kms_client.encrypt(name=request.key_name, plaintext=plaintext_bytes)

    # The ciphertext is returned in a base64 encoded string.
    ciphertext_bytes = response.ciphertext
    return EncryptionResponse(ciphertext=ciphertext_bytes, key_name=request.key_name)
