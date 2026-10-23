import os
from google.cloud import kms
from security_client import get_kms_client, KMSConfig
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        os.getenv("GCP_PROJECT_ID"),
        os.getenv("GCP_LOCATION_ID"),
        os.getenv("GCP_KEY_RING_ID"),
        os.getenv("GCP_CRYPTO_KEY_ID")
    )

    response = client.decrypt(
        request={"name": key_name, "ciphertext": request.ciphertext}
    )

    return DecryptionResponse(
        plaintext=response.plaintext,
        key_id=key_name,
        algorithm="GOOGLE_SYMMETRIC_ENCRYPTION"
    )