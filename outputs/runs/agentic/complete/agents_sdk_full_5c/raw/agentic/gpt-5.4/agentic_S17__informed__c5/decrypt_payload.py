from __future__ import annotations

from security_client import kms_client
from security_models import CryptoRequest, CryptoResponse, b64encode_str


def decrypt_payload(request: CryptoRequest) -> CryptoResponse:
    client = kms_client()
    response = client.decrypt(
        KeyId=request.key_id,
        CiphertextBlob=request.ciphertext_bytes(),
        EncryptionAlgorithm=request.algorithm or "SYMMETRIC_DEFAULT",
        EncryptionContext=request.encryption_context or {},
    )
    plaintext_bytes = response["Plaintext"]
    return CryptoResponse(
        provider="aws-kms",
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", request.algorithm or "SYMMETRIC_DEFAULT"),
        plaintext=plaintext_bytes.decode("utf-8", errors="replace"),
        plaintext_b64=b64encode_str(plaintext_bytes),
        metadata={
            "aws_region": client.meta.region_name,
            "response_key_id": response["KeyId"],
        },
    )
