from __future__ import annotations

from google.cloud import kms

from security_client import get_kms_client, normalize_key_path
from security_models import DecryptRequest, CryptoResponse


def decrypt_payload(request: DecryptRequest) -> CryptoResponse:
    client = get_kms_client()
    key_name = normalize_key_path(request.key_name)
    ciphertext = request.ciphertext.encode("utf-8")
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return CryptoResponse.from_bytes("plaintext", response.plaintext)


def main() -> None:
    req = DecryptRequest(ciphertext="")
    result = decrypt_payload(req)
    print(result.get_text("plaintext"))


if __name__ == "__main__":
    main()
