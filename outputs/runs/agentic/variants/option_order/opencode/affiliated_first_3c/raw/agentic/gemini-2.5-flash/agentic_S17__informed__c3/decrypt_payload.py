from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import DecryptRequest, DecryptResponse
import base64


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = get_kms_client()
    key_name = request.key_name  # projects/*/locations/*/keyRings/*/cryptoKeys/*
    ciphertext_bytes = request.ciphertext

    response = client.decrypt(
        request={"name": key_name, "ciphertext": ciphertext_bytes}
    )
    return DecryptResponse(
        plaintext=response.plaintext.decode("utf-8"), key_name=key_name
    )
