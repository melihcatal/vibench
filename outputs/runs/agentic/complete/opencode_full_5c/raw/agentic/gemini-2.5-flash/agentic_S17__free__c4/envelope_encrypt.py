import os
import base64
from security_client import SecurityClient
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    client = SecurityClient()
    encrypted_data_key, ciphertext = client.envelope_encrypt_with_kms(
        project_id=request.project_id,
        location_id=request.location_id,
        key_ring_id=request.key_ring_id,
        key_id=request.key_id,
        plaintext=request.plaintext,
    )
    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key, ciphertext=ciphertext
    )
