from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """Decrypts a ciphertext payload using Google Cloud KMS."""
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id
    )

    response = client.decrypt(request=kms_v1.DecryptRequest(name=key_name, ciphertext=request.ciphertext))
    return DecryptionResponse(plaintext=response.plaintext)
