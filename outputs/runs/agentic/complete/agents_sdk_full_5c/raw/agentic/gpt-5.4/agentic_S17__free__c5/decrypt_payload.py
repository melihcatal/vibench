from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import DecryptRequest, DecryptResponse, b64decode_str


def decrypt_payload(
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> DecryptResponse:
    request = DecryptRequest(
        ciphertext_b64=ciphertext_b64,
        encryption_context=encryption_context or {},
    )
    kms = get_kms_client(region_name)
    response = kms.decrypt(
        CiphertextBlob=b64decode_str(request.ciphertext_b64),
        EncryptionContext=request.encryption_context,
    )
    return DecryptResponse(
        key_id=response.get("KeyId"),
        plaintext=response["Plaintext"].decode("utf-8"),
    )
