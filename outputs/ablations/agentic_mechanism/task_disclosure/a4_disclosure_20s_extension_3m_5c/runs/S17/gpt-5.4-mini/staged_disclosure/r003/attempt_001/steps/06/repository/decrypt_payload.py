import base64
import os
from typing import Union

from google.cloud import kms_v1


def decrypt_payload(ciphertext: Union[str, bytes], key_name: str | None = None) -> bytes:
    if isinstance(ciphertext, str):
        ciphertext_bytes = base64.b64decode(ciphertext)
    else:
        ciphertext_bytes = ciphertext

    if key_name is None:
        key_name = os.environ["GOOGLE_CLOUD_KMS_KEY_NAME"]

    client = kms_v1.KeyManagementServiceClient()
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext_bytes})
    return response.plaintext
