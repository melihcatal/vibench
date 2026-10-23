from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import DecryptResponse, b64decode_text


def decrypt_payload(
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
) -> DecryptResponse:
    client = get_kms_client()
    response = client.decrypt(
        CiphertextBlob=b64decode_text(ciphertext_b64),
        EncryptionContext=encryption_context or {},
    )
    return DecryptResponse(
        key_id=response["KeyId"],
        plaintext=response["Plaintext"].decode("utf-8"),
    )
