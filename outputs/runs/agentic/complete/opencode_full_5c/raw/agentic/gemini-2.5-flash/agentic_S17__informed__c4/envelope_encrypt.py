import os
from security_client import KMSClient
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt_with_kms(
    key_id: str, plaintext: bytes, aad: bytes = None
) -> EnvelopeEncryptResponse:
    kms_client = KMSClient()
    request = EnvelopeEncryptRequest(
        key_id=key_id, plaintext=plaintext, additional_authenticated_data=aad
    )
    response = kms_client.envelope_encrypt(request)
    return response
