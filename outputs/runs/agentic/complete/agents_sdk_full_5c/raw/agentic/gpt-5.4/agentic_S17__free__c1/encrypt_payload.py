from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse, b64encode_str


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    kms = get_kms_client()
    response = kms.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=request.encryption_context or {},
    )
    return EncryptResponse(
        key_id=response["KeyId"],
        ciphertext_b64=b64encode_str(response["CiphertextBlob"]),
        provider="aws-kms",
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
    )


def run(key_id: str, plaintext: str, encryption_context: Optional[Dict[str, str]] = None) -> dict:
    result = encrypt_payload(
        EncryptRequest(key_id=key_id, plaintext=plaintext, encryption_context=encryption_context)
    )
    return result.__dict__
