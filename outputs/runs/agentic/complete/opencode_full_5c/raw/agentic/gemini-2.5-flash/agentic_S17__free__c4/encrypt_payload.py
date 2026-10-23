import os
import base64
from security_client import SecurityClient
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = SecurityClient()
    ciphertext = client.encrypt_with_kms(
        project_id=request.project_id,
        location_id=request.location_id,
        key_ring_id=request.key_ring_id,
        key_id=request.key_id,
        plaintext=request.plaintext,
    )
    return EncryptResponse(ciphertext=ciphertext)
