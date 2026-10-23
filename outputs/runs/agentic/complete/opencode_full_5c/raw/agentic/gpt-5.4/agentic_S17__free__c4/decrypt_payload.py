from __future__ import annotations

from typing import Any, Dict

from security_client import (
    kms_client,
    normalize_encryption_context,
    provider_name,
    resolve_key_id,
)
from security_models import (
    DecryptPayloadRequest,
    DecryptPayloadResponse,
    from_b64,
    sha256_text,
    utc_now_iso,
)


def decrypt_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = DecryptPayloadRequest(
        key_id=resolve_key_id(payload.get("key_id")),
        ciphertext_b64=payload["ciphertext_b64"],
        encryption_context=normalize_encryption_context(
            payload.get("encryption_context")
        ),
    )
    response = kms_client().decrypt(
        KeyId=request.key_id,
        CiphertextBlob=from_b64(request.ciphertext_b64),
        EncryptionContext=request.encryption_context,
    )
    plaintext = response["Plaintext"].decode("utf-8")
    result = DecryptPayloadResponse(
        provider=provider_name(),
        key_id=response["KeyId"],
        plaintext=plaintext,
        plaintext_sha256=sha256_text(plaintext),
        verified_context=request.encryption_context,
        decrypted_at=utc_now_iso(),
    )
    return result.to_dict()
