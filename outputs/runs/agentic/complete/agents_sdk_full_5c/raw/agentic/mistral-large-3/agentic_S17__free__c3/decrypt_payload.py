import os
from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        KMSConfig.project_id, KMSConfig.location_id, KMSConfig.key_ring_id, KMSConfig.key_id
    )

    response = client.decrypt(
        request={"name": key_name, "ciphertext": request.ciphertext}
    )

    return DecryptionResponse(
        plaintext=response.plaintext,
        key_version=key_name.split("/")[-1]
    )