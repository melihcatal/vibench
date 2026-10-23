from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client, kms_key_name
from security_models import EncryptionRequest, EncryptionResponse, b64encode_str


def encrypt_payload(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EncryptionResponse:
    request = EncryptionRequest(
        key_id=key_id or kms_key_name(),
        plaintext=plaintext,
        encryption_context=encryption_context or {},
    )
    client = get_kms_client()
    response = client.encrypt(
        request={
            "name": request.key_id,
            "plaintext": request.plaintext.encode("utf-8"),
            "additional_authenticated_data": str(request.encryption_context).encode("utf-8"),
        }
    )
    return EncryptionResponse(
        key_id=request.key_id,
        ciphertext_b64=b64encode_str(response.ciphertext),
    )
