import base64
import os
from typing import Union

from google.cloud import kms


def encrypt_payload(plaintext: Union[str, bytes]) -> str:
    key_name = os.environ["GOOGLE_CLOUD_KMS_KEY_NAME"]
    client = kms.KeyManagementServiceClient()
    payload = plaintext.encode("utf-8") if isinstance(plaintext, str) else plaintext
    response = client.encrypt(request={"name": key_name, "plaintext": payload})
    return base64.b64encode(response.ciphertext).decode("ascii")
