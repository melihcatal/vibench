from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse
import base64


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = get_kms_client()
    key_name = request.key_name  # projects/*/locations/*/keyRings/*/cryptoKeys/*
    plaintext_bytes = request.plaintext.encode("utf-8")

    response = client.encrypt(request={"name": key_name, "plaintext": plaintext_bytes})
    return EncryptResponse(ciphertext=response.ciphertext, key_name=key_name)
