from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """Encrypts a plaintext payload using Google Cloud KMS."""
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, request.location_id, request.key_ring_id, request.key_id
    )

    # Convert plaintext to bytes if it's a string
    if isinstance(request.plaintext, str):
        plaintext_bytes = request.plaintext.encode('utf-8')
    else:
        plaintext_bytes = request.plaintext

    response = client.encrypt(request=kms_v1.EncryptRequest(name=key_name, plaintext=plaintext_bytes))
    return EncryptionResponse(ciphertext=response.ciphertext)
