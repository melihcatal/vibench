import base64
import os
import sys

from google.cloud import kms_v1


def encrypt_payload(plaintext: str) -> str:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    location_id = os.environ["GOOGLE_KMS_LOCATION_ID"]
    key_ring_id = os.environ["GOOGLE_KMS_KEY_RING_ID"]
    crypto_key_id = os.environ["GOOGLE_KMS_CRYPTO_KEY_ID"]

    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.encrypt(request={"name": key_name, "plaintext": plaintext.encode("utf-8")})
    return base64.b64encode(response.ciphertext).decode("ascii")


def main() -> None:
    plaintext = sys.stdin.read()
    if not plaintext:
        raise SystemExit(1)
    sys.stdout.write(encrypt_payload(plaintext))


if __name__ == "__main__":
    main()
