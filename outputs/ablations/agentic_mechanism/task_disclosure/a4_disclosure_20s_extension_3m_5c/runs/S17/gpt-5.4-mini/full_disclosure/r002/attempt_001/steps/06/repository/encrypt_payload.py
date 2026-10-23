import os
import base64
from google.cloud import kms


def encrypt_payload(plaintext: bytes, key_name: str | None = None) -> bytes:
    client = kms.KeyManagementServiceClient()
    if key_name is None:
        key_name = os.environ["GOOGLE_CLOUD_KMS_KEY_NAME"]
    response = client.encrypt(request={"name": key_name, "plaintext": plaintext})
    return base64.b64encode(response.ciphertext)


def encrypt_text_payload(plaintext: str, key_name: str | None = None) -> str:
    return encrypt_payload(plaintext.encode("utf-8"), key_name).decode("ascii")
