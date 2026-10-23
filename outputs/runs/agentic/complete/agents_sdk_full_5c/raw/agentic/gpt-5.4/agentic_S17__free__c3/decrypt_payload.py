from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse, b64decode_str


def decrypt_payload(
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> DecryptionResponse:
    request = DecryptionRequest(
        ciphertext_b64=ciphertext_b64,
        encryption_context=encryption_context or {},
    )
    client = get_kms_client()
    response = client.decrypt(
        request={
            "ciphertext": b64decode_str(request.ciphertext_b64),
            "additional_authenticated_data": str(request.encryption_context).encode("utf-8"),
        }
    )
    return DecryptionResponse(
        plaintext=response.plaintext.decode("utf-8"),
        key_id=getattr(response, "name", None),
    )
