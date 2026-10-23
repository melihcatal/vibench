from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import DecryptRequest, DecryptResponse, b64decode_str


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    kms = get_kms_client()
    response = kms.decrypt(
        CiphertextBlob=b64decode_str(request.ciphertext_b64),
        EncryptionContext=request.encryption_context or {},
    )
    return DecryptResponse(
        key_id=response["KeyId"],
        plaintext=response["Plaintext"].decode("utf-8"),
        provider="aws-kms",
    )


def run(ciphertext_b64: str, encryption_context: Optional[Dict[str, str]] = None) -> dict:
    result = decrypt_payload(
        DecryptRequest(ciphertext_b64=ciphertext_b64, encryption_context=encryption_context)
    )
    return result.__dict__
