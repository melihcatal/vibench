from __future__ import annotations

from typing import Dict, Optional

from security_client import get_kms_client, load_encryption_context
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> DecryptResponse:
    request = DecryptRequest(
        ciphertext_b64=ciphertext_b64,
        encryption_context=load_encryption_context(encryption_context),
    )
    kms = get_kms_client(region_name=region_name)
    response = kms.decrypt(
        CiphertextBlob=request.ciphertext_bytes(),
        EncryptionContext=request.encryption_context,
    )
    return DecryptResponse.from_plaintext(
        key_id=response["KeyId"],
        encryption_algorithm=response["EncryptionAlgorithm"],
        plaintext=response["Plaintext"],
    )
