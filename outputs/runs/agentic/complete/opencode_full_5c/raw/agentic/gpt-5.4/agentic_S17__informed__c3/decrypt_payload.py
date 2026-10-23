from __future__ import annotations

from security_client import aws_kms_client
from security_models import DecryptRequest, DecryptResponse, b64decode_text, sha256_hex


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = aws_kms_client()
    response = (
        client.decrypt(
            CiphertextBlob=b64decode_text(request.ciphertext),
            EncryptionContext=request.encryption_context or {},
            KeyId=request.key_id,
        )
        if request.key_id
        else client.decrypt(
            CiphertextBlob=b64decode_text(request.ciphertext),
            EncryptionContext=request.encryption_context or {},
        )
    )
    plaintext = response["Plaintext"]
    return DecryptResponse(
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        plaintext=plaintext.decode("utf-8"),
        plaintext_sha256=sha256_hex(plaintext),
        provider="aws-kms",
    )
