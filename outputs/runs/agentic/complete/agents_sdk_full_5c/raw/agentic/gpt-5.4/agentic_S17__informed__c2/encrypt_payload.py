from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client, get_kms_key_id
from security_models import EncryptResponse, b64encode_bytes


def encrypt_payload(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EncryptResponse:
    client = get_kms_client()
    resolved_key_id = get_kms_key_id(key_id)
    response = client.encrypt(
        KeyId=resolved_key_id,
        Plaintext=plaintext.encode("utf-8"),
        EncryptionContext=encryption_context or {},
    )
    return EncryptResponse(
        key_id=response["KeyId"],
        ciphertext_b64=b64encode_bytes(response["CiphertextBlob"]),
    )
