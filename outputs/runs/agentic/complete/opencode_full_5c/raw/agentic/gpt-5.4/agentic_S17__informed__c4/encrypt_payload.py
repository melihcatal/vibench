from __future__ import annotations

from typing import Any, Dict, Optional

from security_client import get_kms_client, load_encryption_context
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(
    plaintext: Any,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> EncryptResponse:
    request = EncryptRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_context=load_encryption_context(encryption_context),
    )
    kms = get_kms_client(region_name=region_name)
    response = kms.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext_bytes(),
        EncryptionContext=request.encryption_context,
    )
    return EncryptResponse.from_ciphertext(
        key_id=response["KeyId"],
        algorithm=response["EncryptionAlgorithm"],
        ciphertext=response["CiphertextBlob"],
        encryption_context=request.encryption_context,
    )
