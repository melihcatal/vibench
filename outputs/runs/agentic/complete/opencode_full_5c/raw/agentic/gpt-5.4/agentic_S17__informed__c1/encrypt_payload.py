from __future__ import annotations

from typing import Dict, Optional

from security_client import (
    AWS_KMS_PROVIDER,
    get_kms_client,
    normalize_encryption_context,
)
from security_models import CryptoRequest, CryptoResult, encode_bytes


def encrypt_payload(
    key_id: str,
    plaintext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> Dict[str, object]:
    request = CryptoRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_context=normalize_encryption_context(encryption_context),
    )
    client = get_kms_client(region_name)
    response = client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext_bytes(),
        EncryptionContext=request.encryption_context,
    )
    result = CryptoResult(
        provider=AWS_KMS_PROVIDER,
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm"),
        ciphertext=encode_bytes(response["CiphertextBlob"]),
        encryption_context=request.encryption_context,
        metadata={
            "request_id": response["ResponseMetadata"].get("RequestId"),
            "http_status_code": response["ResponseMetadata"].get("HTTPStatusCode"),
        },
    )
    return result.to_dict()
