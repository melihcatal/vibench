from __future__ import annotations

from security_client import kms_client
from security_models import CryptoRequest, CryptoResponse, b64encode_str


def encrypt_payload(request: CryptoRequest) -> CryptoResponse:
    client = kms_client()
    response = client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext_as_bytes(),
        EncryptionAlgorithm=request.algorithm or "SYMMETRIC_DEFAULT",
        EncryptionContext=request.encryption_context or {},
    )
    return CryptoResponse(
        provider="aws-kms",
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", request.algorithm or "SYMMETRIC_DEFAULT"),
        ciphertext_b64=b64encode_str(response["CiphertextBlob"]),
        metadata={
            "aws_region": client.meta.region_name,
            "response_key_id": response["KeyId"],
        },
    )
