import os
from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        os.getenv("GCP_PROJECT_ID"),
        os.getenv("GCP_LOCATION_ID"),
        os.getenv("GCP_KEY_RING_ID"),
        os.getenv("GCP_CRYPTO_KEY_ID")
    )

    response = client.encrypt(
        request={"name": key_name, "plaintext": request.plaintext}
    )

    return EncryptionResponse(
        ciphertext=response.ciphertext,
        key_id=key_name,
        algorithm="GOOGLE_SYMMETRIC_ENCRYPTION"
    )