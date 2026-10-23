import os
from security_client import KMSClient
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload_with_kms(
    key_id: str, ciphertext: bytes, aad: bytes = None
) -> DecryptResponse:
    kms_client = KMSClient()
    request = DecryptRequest(
        key_id=key_id, ciphertext=ciphertext, additional_authenticated_data=aad
    )
    response = kms_client.decrypt_payload(request)
    return response
