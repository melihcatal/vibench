from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client
from security_models import EncryptRequest, EncryptResponse, b64encode_str


def encrypt_payload(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> EncryptResponse:
    request = EncryptRequest(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context or {},
    )
    kms = get_kms_client(region_name)
    response = kms.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=request.encryption_context,
    )
    return EncryptResponse(
        key_id=response["KeyId"],
        ciphertext_b64=b64encode_str(response["CiphertextBlob"]),
        encryption_context=request.encryption_context,
    )
