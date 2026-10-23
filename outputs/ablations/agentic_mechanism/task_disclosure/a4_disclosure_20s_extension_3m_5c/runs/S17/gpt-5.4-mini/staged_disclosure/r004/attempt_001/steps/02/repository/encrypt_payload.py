import base64
import os
from typing import Optional

from google.cloud import kms_v1


def encrypt_payload(plaintext: str, key_name: Optional[str] = None) -> str:
    client = kms_v1.KeyManagementServiceClient()
    if key_name is None:
        key_name = os.environ["GOOGLE_CLOUD_KMS_KEY_NAME"]
    response = client.encrypt(request={"name": key_name, "plaintext": plaintext.encode("utf-8")})
    return base64.b64encode(response.ciphertext).decode("utf-8")


if __name__ == "__main__":
    import sys

    payload = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PLAINTEXT_PAYLOAD", "")
    print(encrypt_payload(payload))
