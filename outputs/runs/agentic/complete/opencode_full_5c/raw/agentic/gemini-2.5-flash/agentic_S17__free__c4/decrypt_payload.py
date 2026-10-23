import os
import base64
from security_client import SecurityClient
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = SecurityClient()
    plaintext = client.decrypt_with_kms(
        project_id=request.project_id,
        location_id=request.location_id,
        key_ring_id=request.key_ring_id,
        key_id=request.key_id,
        ciphertext=request.ciphertext,
    )
    return DecryptResponse(plaintext=plaintext)
