from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse, b64decode_to_bytes


def decrypt_payload(
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> DecryptionResponse:
    request = DecryptionRequest(
        ciphertext_b64=ciphertext_b64,
        encryption_context=encryption_context or {},
    )
    kms = get_kms_client()
    response = kms.decrypt(
        CiphertextBlob=b64decode_to_bytes(request.ciphertext_b64),
        EncryptionContext=request.encryption_context,
    )
    return DecryptionResponse(
        key_id=response["KeyId"],
        plaintext=response["Plaintext"].decode("utf-8"),
    )
