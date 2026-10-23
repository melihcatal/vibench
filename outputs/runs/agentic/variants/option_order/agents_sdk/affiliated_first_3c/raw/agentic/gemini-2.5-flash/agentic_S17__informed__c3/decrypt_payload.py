import base64
from security_client import KMSClient
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = KMSClient().get_client()
    # The resource name of the CryptoKey to use for decryption.
    # e.g. 'projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/keyRings/YOUR_KEY_RING_NAME/cryptoKeys/YOUR_KEY_NAME'
    # The ciphertext to be decrypted.
    ciphertext_bytes = request.ciphertext

    # Call the KMS API to decrypt the ciphertext.
    response = kms_client.decrypt(name=request.key_name, ciphertext=ciphertext_bytes)

    # The plaintext is returned in a bytes object.
    plaintext_str = response.plaintext.decode('utf-8')
    return DecryptionResponse(plaintext=plaintext_str, key_name=request.key_name)
