from __future__ import annotations

import base64
from google.cloud import kms

from security_client import get_kms_client, normalize_key_path
from security_models import EncryptRequest, CryptoResponse


def encrypt_payload(request: EncryptRequest) -> CryptoResponse:
    client = get_kms_client()
    key_name = normalize_key_path(request.key_name)
    plaintext = request.plaintext.encode("utf-8")
    response = client.encrypt(request={"name": key_name, "plaintext": plaintext})
    return CryptoResponse.from_bytes("ciphertext", response.ciphertext)


def main() -> None:
    req = EncryptRequest(plaintext="managed-key payload")
    result = encrypt_payload(req)
    print(result.get_text("ciphertext"))


if __name__ == "__main__":
    main()
