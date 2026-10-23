import base64
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """Decrypts a ciphertext payload using a GCP KMS key."""
    client = get_kms_client()

    decoded_ciphertext = base64.b64decode(request.ciphertext)

    response = client.decrypt(
        request={"name": request.key_name, "ciphertext": decoded_ciphertext}
    )

    return DecryptionResponse(key_name=request.key_name, plaintext=response.plaintext)
