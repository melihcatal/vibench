import os
from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id, 
        request.location_id, 
        request.key_ring_id, 
        request.key_id
    )

    response = client.decrypt(
        request={
            "name": key_name,
            "ciphertext": request.ciphertext
        }
    )

    return DecryptionResponse(
        plaintext=response.plaintext.decode()
    )