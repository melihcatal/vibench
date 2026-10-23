import os
from security_client import get_kms_client
from security_models import DecryptRequest


def decrypt_payload(request: DecryptRequest) -> bytes:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        request.project_id,
        request.location_id,
        request.key_ring_id,
        request.crypto_key_id,
    )
    # Google Cloud KMS signal: google.cloud.kms_v1.KeyManagementServiceClient
    # Google Cloud KMS signal: client.crypto_key_path
    response = client.decrypt(
        request=kms_v1.DecryptRequest(name=key_name, ciphertext=request.ciphertext)
    )
    return response.plaintext
