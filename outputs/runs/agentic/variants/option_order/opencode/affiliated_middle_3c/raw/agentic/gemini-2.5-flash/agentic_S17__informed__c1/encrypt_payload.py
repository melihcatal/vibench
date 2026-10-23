import os
from security_client import KmsClient
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    client = KmsClient().get_client()
    # The KMS key to use for encryption. Expected format:
    # projects/PROJECT_ID/locations/LOCATION_ID/keyRings/KEY_RING_ID/cryptoKeys/CRYPTO_KEY_ID
    key_name = request.key_name
    plaintext_bytes = request.plaintext.encode("utf-8")

    try:
        response = client.encrypt(
            request={"name": key_name, "plaintext": plaintext_bytes}
        )
        return EncryptionResponse(
            ciphertext=response.ciphertext.hex(), key_name=key_name
        )
    except Exception as e:
        raise RuntimeError(f"Failed to encrypt payload with Google Cloud KMS: {e}")
