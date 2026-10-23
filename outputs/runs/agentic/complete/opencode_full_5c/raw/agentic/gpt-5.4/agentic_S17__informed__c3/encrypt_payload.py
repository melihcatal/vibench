from __future__ import annotations

from security_client import aws_kms_client, kms_key_id
from security_models import (
    EncryptRequest,
    EncryptResponse,
    b64encode_bytes,
    normalize_plaintext,
    sha256_hex,
)


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    plaintext = normalize_plaintext(request.plaintext)
    client = aws_kms_client()
    key_id = kms_key_id(request.key_id)
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext,
        EncryptionContext=request.encryption_context or {},
    )
    return EncryptResponse(
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        ciphertext=b64encode_bytes(response["CiphertextBlob"]),
        plaintext_sha256=sha256_hex(plaintext),
        provider="aws-kms",
    )
