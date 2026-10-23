from __future__ import annotations

import os
from google.cloud import kms
from cryptography.fernet import Fernet

from security_client import get_kms_client, normalize_key_path
from security_models import EnvelopeEncryptRequest, CryptoResponse


def envelope_encrypt(request: EnvelopeEncryptRequest) -> CryptoResponse:
    client = get_kms_client()
    key_name = normalize_key_path(request.key_name)
    dek = Fernet.generate_key()
    fernet = Fernet(dek)
    encrypted_payload = fernet.encrypt(request.plaintext.encode("utf-8"))
    wrapped_dek = client.encrypt(request={"name": key_name, "plaintext": dek})
    result = {
        "wrapped_dek": CryptoResponse.from_bytes("wrapped_dek", wrapped_dek.ciphertext).get_text("wrapped_dek"),
        "ciphertext": encrypted_payload.decode("utf-8"),
        "aad": request.aad or "",
        "provider": "google-cloud-kms",
        "hostname": "cloudkms.googleapis.com",
    }
    return CryptoResponse(result)


def main() -> None:
    req = EnvelopeEncryptRequest(plaintext="envelope encryption example")
    print(envelope_encrypt(req).data)


if __name__ == "__main__":
    main()
