import base64
import os
from typing import Optional

from google.cloud import kms_v1


def encrypt_payload(plaintext: str, key_name: str, location: Optional[str] = None) -> str:
    client = kms_v1.KeyManagementServiceClient()
    payload = plaintext.encode("utf-8")
    response = client.encrypt(request={"name": key_name, "plaintext": payload})
    return base64.b64encode(response.ciphertext).decode("ascii")


def main() -> None:
    plaintext = os.environ.get("PLAINTEXT", "")
    key_name = os.environ["GOOGLE_CLOUD_KMS_KEY_NAME"]
    print(encrypt_payload(plaintext, key_name))


if __name__ == "__main__":
    main()
