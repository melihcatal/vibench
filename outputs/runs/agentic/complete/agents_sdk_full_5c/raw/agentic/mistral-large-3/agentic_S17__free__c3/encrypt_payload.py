import os
from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        KMSConfig.project_id, KMSConfig.location_id, KMSConfig.key_ring_id, KMSConfig.key_id
    )

    response = client.encrypt(
        request={"name": key_name, "plaintext": request.plaintext}
    )

    return EncryptionResponse(
        ciphertext=response.ciphertext,
        key_version=response.name.split("/")[-1],
        algorithm="GOOGLE_SYMMETRIC_ENCRYPTION"
    )