from __future__ import annotations

from typing import Dict, Optional

from security_client import (
    AWS_KMS_PROVIDER,
    get_kms_client,
    normalize_encryption_context,
)
from security_models import CryptoRequest, CryptoResult, decode_bytes, encode_bytes


def decrypt_payload(
    key_id: str,
    ciphertext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> Dict[str, object]:
    request = CryptoRequest(
        key_id=key_id,
        ciphertext=ciphertext,
        encryption_context=normalize_encryption_context(encryption_context),
    )
    client = get_kms_client(region_name)
    response = client.decrypt(
        KeyId=request.key_id,
        CiphertextBlob=decode_bytes(request.ciphertext or ""),
        EncryptionContext=request.encryption_context,
    )
    plaintext_bytes = response["Plaintext"]
    result = CryptoResult(
        provider=AWS_KMS_PROVIDER,
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm"),
        plaintext=plaintext_bytes.decode("utf-8"),
        plaintext_base64=encode_bytes(plaintext_bytes),
        encryption_context=request.encryption_context,
        metadata={
            "request_id": response["ResponseMetadata"].get("RequestId"),
            "http_status_code": response["ResponseMetadata"].get("HTTPStatusCode"),
        },
    )
    return result.to_dict()
