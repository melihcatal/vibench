import base64
from google.cloud import kms
from security_models import DecryptionRequest, DecryptionResponse
from security_client import KmsClient

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = KmsClient()
    client = kms_client.client

    name = kms_client.get_key_path(request.project_id, request.location, request.key_ring, request.key_id)

    # The ciphertext from the request will be base64 encoded, decode it first
    ciphertext_bytes = base64.b64decode(request.ciphertext)

    response = client.decrypt(request={"name": name, "ciphertext": ciphertext_bytes})
    return DecryptionResponse(plaintext=response.plaintext)
