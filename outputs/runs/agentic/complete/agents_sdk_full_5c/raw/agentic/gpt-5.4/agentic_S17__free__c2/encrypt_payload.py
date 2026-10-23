from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client, get_kms_key_id
from security_models import EncryptionRequest, EncryptionResponse, b64encode_bytes


def encrypt_payload(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EncryptionResponse:
    request = EncryptionRequest(
        plaintext=plaintext,
        key_id=get_kms_key_id(key_id),
        encryption_context=encryption_context or {},
    )
    kms = get_kms_client()
    response = kms.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=request.encryption_context,
    )
    return EncryptionResponse(
        key_id=response["KeyId"],
        ciphertext_b64=b64encode_bytes(response["CiphertextBlob"]),
        algorithm=response.get("EncryptionAlgorithm"),
    )
