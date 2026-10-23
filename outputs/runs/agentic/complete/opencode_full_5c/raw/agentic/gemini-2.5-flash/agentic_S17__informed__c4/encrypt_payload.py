import os
from security_client import KMSClient
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload_with_kms(
    key_id: str, plaintext: bytes, aad: bytes = None
) -> EncryptResponse:
    kms_client = KMSClient()
    request = EncryptRequest(
        key_id=key_id, plaintext=plaintext, additional_authenticated_data=aad
    )
    response = kms_client.encrypt_payload(request)
    return response
