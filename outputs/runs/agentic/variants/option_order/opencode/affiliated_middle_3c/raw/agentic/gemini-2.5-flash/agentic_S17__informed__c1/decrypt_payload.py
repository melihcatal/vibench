import os
import binascii
from security_client import KmsClient
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = KmsClient().get_client()
    # The KMS key to use for decryption. Expected format:
    # projects/PROJECT_ID/locations/LOCATION_ID/keyRings/KEY_RING_ID/cryptoKeys/CRYPTO_KEY_ID
    key_name = request.key_name
    ciphertext_bytes = binascii.unhexlify(request.ciphertext)

    try:
        response = client.decrypt(
            request={"name": key_name, "ciphertext": ciphertext_bytes}
        )
        return DecryptionResponse(
            plaintext=response.plaintext.decode("utf-8"), key_name=key_name
        )
    except Exception as e:
        raise RuntimeError(f"Failed to decrypt payload with Google Cloud KMS: {e}")
